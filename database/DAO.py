from database.DB_connect import DBConnect
from model.classification import Classification
from model.gene import Gene
from model.interaction import Interaction


class DAO():

    @staticmethod
    def get_all_genes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                        FROM genes"""
            cursor.execute(query)

            for row in cursor:
                result.append(Gene(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_interactions():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                           FROM interactions"""
            cursor.execute(query)

            for row in cursor:
                result.append(Interaction(**row))

            cursor.close()
            cnx.close()
        return result

    # @staticmethod
    # def get_all_classifications():
    #     cnx = DBConnect.get_connection()
    #     result = []
    #     if cnx is None:
    #         print("Connessione fallita")
    #     else:
    #         cursor = cnx.cursor(dictionary=True)
    #         query = """SELECT *
    #                     FROM classification"""
    #         cursor.execute(query)
    #
    #         for row in cursor:
    #             result.append(Classification(**row))
    #
    #         cursor.close()
    #         cnx.close()
    #     return result

    @staticmethod
    def getAllLocalization():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """select distinct c.Localization
                        from classification c 
                        order by c.Localization desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["Localization"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllNodes( localization):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """ select g.GeneID , c.Localization, g.Essential
                        from classification c, genes g
                        where c.GeneID = g.GeneID
                        and c.Localization = %s
                        group by g.GeneID, g.Essential"""
            cursor.execute(query, (localization, ) )

            for row in cursor:
                #result.append(Classification(row["GeneID"], row["Localization"], row["Essential"]))
                result.append(Classification(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getEdgeWeight(g1, g2):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """ select sum(a.chromosome) as peso
                        from (select g1.Chromosome
                                from genes g1
                                where g1.GeneID = %s
                                union 
                                select g2.Chromosome
                                from genes g2
                                where g2.GeneID = %s ) as a"""
            cursor.execute(query, (g1, g2))

            for row in cursor:
                result.append(row["peso"])

            cursor.close()
            cnx.close()
        return result




