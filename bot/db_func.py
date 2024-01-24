from loguru import logger
import uuid

from database.conn import session
from models.graph_models import Graphic
from models.geo_map_models import GeoMap
from models.related_entities_models import RelatedEntitiesTop, RelatedEntitiesRising
from models.related_queries_models import RelatedQueriesTop, RelatedQueriesRising


class DatabaseFunctions():
    
    def save_multi_timeline(param, data, hora, valor):
        new_uuid = uuid.uuid4()

        data_graphic_trends = Graphic(
                uuid = new_uuid,
                name=param,
                date=data,
                hour=hora,
                value=str(valor)
            )          

        try:
            logger.success("Salvando no banco de dados Interesse ao Longo do Tempo")
            with session.begin_nested():
                existing_record = session.query(Graphic).filter_by(
                    name=param,
                    date=data,
                    hour=hora,
                    value=str(valor)
                ).one_or_none()

            if existing_record:
                existing_record.value = str(valor)
                existing_record.date = data 
                existing_record.hour = hora
            else:
                session.merge(data_graphic_trends)

            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao inserir/atualizar registro: {str(e)}")  


    
    def save_region(param, data_inicio, data_fim, region, value_region):
        new_uuid = uuid.uuid4()

        geo_map_trends = GeoMap(
                uuid = new_uuid,
                param=param,
                initial_date=data_inicio,
                end_date=data_fim,
                region=region,
                value=str(value_region)
            )          
        
        try:
            logger.info("Salvando no banco de dados Sub-Região")
            with session.begin_nested():
                existing_record = session.query(GeoMap).filter_by(
                    param=param,
                    initial_date=data_inicio,
                    end_date=data_fim,
                    region=region,
                    value=str(value_region)
                ).one_or_none()

            if existing_record:
                existing_record.initial_date = data_inicio
                existing_record.end_date = data_fim
                existing_record.region = region 
                existing_record.value = str(value_region)
            else:
                session.merge(geo_map_trends)

            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao inserir/atualizar registro de Sub-Região: {str(e)}")


    def save_related_entities_top(param, country, data_inicio, data_fim, entities, value_related_entities):
        new_uuid = uuid.uuid4()

        related_entities = RelatedEntitiesTop(
                uuid = new_uuid,
                param=param,
                region=country,
                initial_date=data_inicio,
                end_date=data_fim,
                entities=entities,
                value=str(value_related_entities)
            )          
        
        try:
            logger.info("Salvando no banco de dados Assuntos Relacionados TOP")
            with session.begin_nested():
                existing_record = session.query(RelatedEntitiesTop).filter_by(
                    param=param,
                    region=country,
                    initial_date=data_inicio,
                    end_date=data_fim,
                    entities=entities,
                    value=str(value_related_entities)
                ).one_or_none()

            if existing_record:
                existing_record.region = country 
                existing_record.initial_date = data_inicio
                existing_record.end_date = data_fim
                existing_record.entities = entities
                existing_record.value = value_related_entities
            else:
                session.merge(related_entities)

            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao inserir/atualizar registro na tabela de Assuntos Relacionados Top {str(e)}")


    
    def save_related_entities_rising(param, country, data_inicio, data_fim, entity, value):
        new_uuid = uuid.uuid4()

        related_entities_rising = RelatedEntitiesRising(
                uuid = new_uuid,
                param=param,
                region=country,
                initial_date=data_inicio,
                end_date=data_fim,
                entities=entity,
                value=str(value)
            )          
        
        try:
            logger.info("Salvando no banco de dados Assuntos Relacionados RISING")
            with session.begin_nested():
                existing_record = session.query(RelatedEntitiesRising).filter_by(
                    param=param,
                    region=country,
                    initial_date=data_inicio,
                    end_date=data_fim,
                    entities=entity,
                    value=str(value)
                ).one_or_none()

            if existing_record:
                existing_record.region = country 
                existing_record.initial_date = data_inicio
                existing_record.end_date = data_fim
                existing_record.entities = entity
                existing_record.value = str(value)
            else:
                session.merge(related_entities_rising)

            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao inserir/atualizar registro Assuntos Relacionados RISING: {str(e)}")


    def save_related_queries_top(param, country, data_inicio, data_fim, entities, value_related_entities, value_related_queries):
        new_uuid = uuid.uuid4()

        related_queries = RelatedQueriesTop(
                uuid = new_uuid,
                param=param,
                region=country,
                initial_date=data_inicio,
                end_date=data_fim,
                queries=entities,
                value=str(value_related_entities)
            )          
        
        try:
            logger.info("Salvando no banco de dados Pesquisas Relacionadas TOP")
            with session.begin_nested():
                existing_record = session.query(RelatedQueriesTop).filter_by(
                    param=param,
                    region=country,
                    initial_date=data_inicio,
                    end_date=data_fim,
                    queries=entities,
                    value=str(value_related_queries)
                ).one_or_none()

            if existing_record:
                existing_record.region = country
                existing_record.initial_date = data_inicio
                existing_record.end_date = data_fim
                existing_record.queries = entities
                existing_record.value = str(value_related_queries)
            else:
                session.merge(related_queries)

            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao inserir/atualizar registro na tabela de Pesquisas Relacionadas Top {str(e)}")


    def save_related_queries_rising(param, country, data_inicio, data_fim, entity, value):
        new_uuid = uuid.uuid4()

        related_queries_rising = RelatedQueriesRising(
                uuid = new_uuid,
                param=param,
                region=country,
                initial_date=data_inicio,
                end_date=data_fim,
                queries=entity,
                value=str(value)
            )          
        
        try:
            logger.info("Tentando inserir/atualizar registro Pesquisas Relacionadas RISING")
            
            with session.begin_nested():
                existing_record = session.query(RelatedQueriesRising).filter_by(
                    uuid=new_uuid,
                    param=param,
                    region=country,
                    initial_date=data_inicio,
                    end_date=data_fim,
                    queries=entity,
                    value=str(value)
                ).one_or_none()

            if existing_record:
                existing_record.region = country
                existing_record.initial_date = data_inicio
                existing_record.end_date = data_fim
                existing_record.queries = entity
                existing_record.value = str(value)
            else:
                session.merge(related_queries_rising)

            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao inserir/atualizar registro Pesquisas Relacionadas RISING: {str(e)}")