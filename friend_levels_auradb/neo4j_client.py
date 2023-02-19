from neo4j import GraphDatabase
from string import Template

def parse_birth(date):
    if len(date) < 8:
        return None
    else:
        arr = date.split('.')
        return {
            'day': int(arr[0]),
            'month': int(arr[1]),
            'year': int(arr[2])
        }


class Client:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_friendship(self, person1, person2):
        with self.driver.session(database="neo4j") as session:
            session.execute_write(self._create_and_return_friendship, person1, person2)

    @staticmethod
    def _create_and_return_friendship(tx, person1, person2):

        bdate1 = parse_birth(person1['bdate'])
        bdate2 = parse_birth(person2['bdate'])

        query = (
            Template("merge (p1:$label {id:$id, first_name: \"$first_name\", last_name: \"$last_name\" }) ")
                .substitute(label=person1['label'], id=person1['id'], first_name=person1['first_name'], last_name=person1['last_name']) +
            (Template("set p1.bdate = date({day: $d, month: $m, year: $y}) ").substitute(d=bdate1['day'], m=bdate1['month'], y=bdate1['year']) if bdate1 is not None else "") +
            Template("merge (p2:$label {id:$id, first_name: \"$first_name\", last_name: \"$last_name\" }) ")
                .substitute(label=person2['label'], id=person2['id'], first_name=person2['first_name'], last_name=person2['last_name']) +
            (Template("set p2.bdate = date({day: $d, month: $m, year: $y}) ").substitute(d=bdate2['day'], m=bdate2['month'], y=bdate2['year']) if bdate2 is not None else "") +
            "merge (p1)-[:FRIENDSHIP]->(p2) "
            "return p1, p2"
        )
        tx.run(query)

    def find_all(self):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_read(self._find_all)
            for row in result:
                print("Found person: {row}".format(row=row))

    @staticmethod
    def _find_all(tx):
        query = (
            "MATCH (n) "
            "RETURN n"
        )
        result = tx.run(query)
        return [row for row in result]
