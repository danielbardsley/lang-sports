docker run \
    --publish=7474:7474 --publish=7687:7687 \
    --volume=$HOME/neo4j/data:/data \
    -e NEO4J_AUTH=neo4j/Password1 \
    -d \
    --name=neo4j \
    neo4j