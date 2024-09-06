from neo4j import GraphDatabase


class SportsGraph:
    def __init__(self, uri, auth):
        self.driver = GraphDatabase.driver(uri, auth=auth)

    def close(self):
        self.driver.close()

    def add_sport(self, sport_id, sport_name):
        with self.driver.session() as session:
            session.execute_write(self._create_sport, sport_id, sport_name)

    @staticmethod
    def _create_sport(tx, sport_id, sport_name):
        query = (
            "MERGE (s:Sport {id: $sport_id, name: $sport_name}) "
            "RETURN s"
        )
        result = tx.run(query, sport_id=sport_id, sport_name=sport_name)
        return result.single()

    def add_competition(self, sport_id, competition_id, competition_name):
        with self.driver.session() as session:
            session.execute_write(self._create_competition, sport_id, competition_id, competition_name)

    @staticmethod
    def _create_competition(tx, sport_id, competition_id, competition_name):
        query = (
            "MATCH (s:Sport {id: $sport_id}) "
            "MERGE (c:Competition {id: $competition_id, name: $competition_name}) "
            "MERGE (c)-[:BELONGS_TO]->(s) "
            "RETURN c"
        )
        result = tx.run(query, sport_id=sport_id, competition_id=competition_id, competition_name=competition_name)
        return result.single()

    def add_event(self, competition_id, event_id, event_name, start_time):
        with self.driver.session() as session:
            session.execute_write(self._create_event, competition_id, event_id, event_name, start_time)

    @staticmethod
    def _create_event(tx, competition_id, event_id, event_name, start_time):
        query = (
            "MATCH (c:Competition {id: $competition_id}) "
            "MERGE (e:Event {id: $event_id, name: $event_name, start_time: $start_time}) "
            "MERGE (e)-[:PART_OF]->(c) "
            "RETURN e"
        )
        result = tx.run(query,
                        competition_id=competition_id, event_id=event_id,
                        event_name=event_name, start_time=start_time)
        return result.single()

    def get_sports(self):
        with self.driver.session() as session:
            return session.execute_read(self._get_sports)

    @staticmethod
    def _get_sports(tx):
        query = "MATCH (s:Sport) RETURN s.name AS sport"
        result = tx.run(query)
        return [record["sport"] for record in result]

    def get_competitions(self, sport_name):
        with self.driver.session() as session:
            return session.execute_read(self._get_competitions, sport_name)

    @staticmethod
    def _get_competitions(tx, sport_name):
        query = (
            "MATCH (s:Sport {name: $sport_name})<-[:BELONGS_TO]-(c:Competition) "
            "RETURN c.name AS competition"
        )
        result = tx.run(query, sport_name=sport_name)
        return [record["competition"] for record in result]

    def get_events(self, competition_name):
        with self.driver.session() as session:
            return session.execute_read(self._get_events, competition_name)

    @staticmethod
    def _get_events(tx, competition_name):
        query = (
            "MATCH (c:Competition {name: $competition_name})<-[:PART_OF]-(e:Event) "
            "RETURN e.name AS event, e.startTime AS startTime"
        )
        result = tx.run(query, competition_name=competition_name)
        return [{"event": record["event"], "startTime": record["startTime"]} for record in result]