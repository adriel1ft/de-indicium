import pyarrow.parquet as pq
import pandas as pd
from sqlalchemy import create_engine, inspect
import os
from tqdm import tqdm  # for progress bar
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_system_schema(schema_name):
    """Identifica schemas do sistema que não devem ser modificados"""
    return schema_name.lower() in ['information_schema', 'pg_catalog']

def load_nested_parquet_to_db(engine, base_path):
    """Carrega arquivos Parquet de estrutura aninhada"""
    logger.info(f"Varrendo diretório base: {base_path}")
    
    # Primeiro passe: identificar todos os arquivos .parquet
    parquet_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.parquet'):
                full_path = os.path.join(root, file)
                parquet_files.append(full_path)
    
    if not parquet_files:
        logger.error("Nenhum arquivo .parquet encontrado!")
        return
    
    logger.info(f"Encontrados {len(parquet_files)} arquivos .parquet")
    
    # Segundo passe: processar cada arquivo
    for file_path in tqdm(parquet_files, desc="Processando arquivos"):
        try:
            # Extrair schema e nome da tabela do caminho
            rel_path = os.path.relpath(file_path, base_path)
            path_parts = rel_path.split(os.sep)
            
            if len(path_parts) > 1:
                schema_table = path_parts[0]
            else:
                schema_table = os.path.basename(file_path).split('-')[0]
            
            # Verificar se o nome contém um schema explícito
            if '-' in schema_table:
                schema, table = schema_table.split('-', 1)
            else:
                schema = 'public'  # Assumir schema padrão como 'public'
                table = schema_table
            
            table = table.split('.')[0]  # Remove extensão se houver
            
            logger.info(f"\nProcessando: {file_path}")
            logger.info(f"Schema: {schema}, Tabela: {table}")
            
            # Ler arquivo Parquet
            df = pq.read_table(file_path).to_pandas()
            logger.info(f"Linhas lidas: {len(df)}")
            
            # Tratamento especial para schemas do sistema
            if is_system_schema(schema):
                logger.warning(f"Pulando schema do sistema: {schema}.{table}")
                continue
                
            # Verificar se a tabela já existe
            inspector = inspect(engine)
            if inspector.has_table(table, schema=schema):
                # Se existir, fazer append em vez de replace
                logger.info(f"Tabela existente detectada, adicionando dados...")
                if_exists = 'append'
            else:
                if_exists = 'fail'
            
            # Inserir os dados no banco de dados
            df.to_sql(
                name=table,
                con=engine,
                schema=schema,
                if_exists=if_exists,
                index=False
            )
            logger.info(f"Sucesso: {schema}.{table}")
            
        except Exception as e:
            logger.error(f"Erro no arquivo {file_path}: {str(e)}")


db_connection = "postgresql://northwind:northwind@localhost:5434/northwind"
engine = create_engine(db_connection)


load_nested_parquet_to_db(engine, 'load/')