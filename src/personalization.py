import base64
import json
from sqlalchemy import func
from db_model import (
    Event,
    EventDuration,
    DBSession,
    Tag,
    EventTag,
    EventRecommendation
)
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity 


def tokenizer(text):
    return map(str.strip, text.split(','))

def personalization(event_id):
    """
    Generate event's vector representation, generate cosine similarity, and store to databasetriggered on event created/updated
    Args:
        event_id: id of the event (integer)
    """

    event_description = ''
    session = DBSession()
    try:
        # query event info 
        query_event = (
            session.query(Event).filter(Event.id == event_id).scalar()
        )
        if query_event is not None:
            event_description = query_event.description
        else:
            raise Exception("Event not found")

        #  convert event description it into vector form 
        sbert_model = SentenceTransformer('src/stsb-roberta-large-model')
        sentence_embeddings = sbert_model.encode(event_description, show_progress_bar =True)

        
        # store event vector into db
        event_vector = session.query(EventRecommendation).filter_by(event_id = event_id).first()
        if not event_vector:
            event_vector = EventRecommendation(
                event_id = event_id,
                event_vector = sentence_embeddings.tolist()
            )
            session.add(event_vector)
        else:
            event_vector.event_vector = sentence_embeddings.tolist()
        
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()



    session = DBSession()
    try:
        # query all events, events_tag, events_vector from DB
        tags_ids = []
        events_ids = []
        vectors = []
        events_vectors = session.query(EventRecommendation).join(EventTag, EventTag.event_id == EventRecommendation.event_id).group_by(EventTag.event_id).with_entities(func.max(EventRecommendation.event_id), func.max(EventRecommendation.event_vector), func.array_agg(EventTag.tag_id))
        if len(events_vectors) == 0:
            raise Exception("No events available to generate recommendation")
        
        for item in events_vectors:
            delimiter = ','
            tags = map(str, item[2])
            tags_ids.append(delimiter.join(tags))
            events_ids.append(item[0])
            vectors.append(item[1])


         # calculate tf-idf
        vectorizer = TfidfVectorizer(tokenizer = tokenizer)
        tf_idf_sparce_array = vectorizer.fit_transform(tags_ids)
        tf_idf_feature = tf_idf_sparce_array.toarray()

        # calculate cosine similarity of tf-idf
        cosine_sim_des_tags = linear_kernel(tf_idf_feature, tf_idf_feature)


        # calculate cosine similarity of event vector
        cosine_sim_des_descriptions = cosine_similarity(vectors, vectors)

        # combine tf-idf with event vector
        cosine_result = np.mean([cosine_sim_des_tags, cosine_sim_des_descriptions], axis = 0)

        # sort cosine similarity
        k_highest_score = []
        k = 50

        for item in cosine_result:
            index_of_score = np.argsort(item)[-k:]
            index_of_score = np.flip(index_of_score)
            result = np.array([np.array(events_ids)[index_of_score], item[index_of_score]]).T
            k_highest_score.append(result)

        # store score to db
        for score in k_highest_score:
            score_result = {}
            for item in score[1:]:
                score_result[int(item[0])] = item[1]
            event_vector = session.query(EventRecommendation).filter_by(event_id = int(score[0][0])).first() 
            event_vector.score = score_result

        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()