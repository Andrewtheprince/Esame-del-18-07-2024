from database.DB_connect import DBConnect
from model.gene import Gene
from model.interaction import Interaction

class DAO:

    @staticmethod
    def getNCromosomi():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary = True)
        query = """ SELECT g.Chromosome
                    FROM genes g
                    group by g.Chromosome
                    order by g.Chromosome asc"""
        cursor.execute(query)
        for row in cursor:
            result.append(row["Chromosome"])
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def get_all_genes(nMin, nMax):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT *
                    FROM genes g
                    WHERE g.Chromosome >= %s and g.Chromosome <= %s """
        cursor.execute(query, (nMin, nMax,))
        for row in cursor:
            result.append(Gene(**row))
        cursor.close()
        conn.close()
        return result


    @staticmethod
    def get_all_interactions(idMap):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ select i.*
                    from interactions i, classification c, classification c2
                    where i.GeneID1 = c.GeneID and i.GeneID2 =c2.GeneID and c.Localization  = c2.Localization 
                    and i.GeneID1 != i.GeneID2"""
        cursor.execute(query)
        for row in cursor:
            if row["GeneID1"] in idMap and row["GeneID2"] in idMap:
                result.append(Interaction(**row))
        cursor.close()
        conn.close()
        return result