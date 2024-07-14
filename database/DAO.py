from database.DB_connect import DBConnect
from model.gene import Gene


class DAO():

    @staticmethod
    def getAllGenes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from genes"""

        cursor.execute(query)

        for row in cursor:
            result.append(Gene(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * 
                    from genes g 
                    WHERE g.Chromosome %2 =0 
                    order by Chromosome asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Gene(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT g1.GeneID as g1id, g2.GeneID as g2id, c1.Localization, c2.Localization, i.Expression_Corr as peso
                    FROM genes g1, genes g2, classification c1, classification c2, interactions i
                    WHERE g1.GeneID = c1.GeneID 
                    and g2.GeneID = c2.GeneID 
                    and c1.Localization = c2.Localization 
                    and g1.Chromosome %2 = 0 
                    and g2.Chromosome %2 = 0 
                    and ((i.GeneID1=g1.GeneID AND i.GeneID2=g2.GeneID)
                         OR (i.GeneID1=g2.GeneID AND i.GeneID2=g1.GeneID)) 
                    and g1.GeneID > g2.GeneID 
                    and  i.Expression_Corr > 0.0 and i.Expression_Corr < 1
                    order by i.Expression_Corr DESC """

        cursor.execute(query)

        for row in cursor:
            result.append((Gene(idMap[row["g1id"]]),Gene(idMap[row["g2id"]]),row["peso"]))

        cursor.close()
        conn.close()
        return result