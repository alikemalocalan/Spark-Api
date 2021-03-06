from pyspark import SparkConf, SparkContext, StorageLevel, Row
from pyspark.sql import SparkSession

conf = (SparkConf()
        .set("spark.executor.cores", "12")
        .set("spark.executor.memory", "5g")
        .setAppName("Spark-API")
        .setMaster("local[*]"))


# master="spark://alikemal-300E5C:7077"
#  spark://192.168.2.106:7077


class InitSpark:
    def __init__(self):
        self.sc = SparkContext(conf=conf)
        locale = self.sc._jvm.java.util.Locale
        locale.setDefault(locale.forLanguageTag("tr-TR"))
        self.sc.setLogLevel("INFO")
        self.spark = SparkSession(self.sc) \
            .builder \
            .config("spark.mongodb.input.uri",
                    "mongodb://alikemal:123456alikemal@alikemal.org:27017/admin.recommend?authMechanism=SCRAM-SHA-1") \
            .config("spark.mongodb.output.uri",
                    "mongodb://alikemal:123456alikemal@alikemal.org:27017/admin.recommend?authMechanism=SCRAM-SHA-1") \
            .config("packages", "org.mongodb.spark:mongo-spark-connector_2.11:2.0.0") \
            .getOrCreate()

        self.base_txt = "dataset/"
        self.usercsv_txt = self.base_txt + "users.json"
        self.oneksongs = self.base_txt + "1ksong.json"
        self.ratingParq = self.base_txt + "rating.json"
        self.song_parqPATH = self.base_txt + "songs.parquet"

        df = self.spark.read.format("com.mongodb.spark.sql.DefaultSource") \
            .option("uri",
                    "mongodb://alikemal:123456alikemal@alikemal.org:27017/admin.historySongs?authMechanism=SCRAM-SHA-1").load()
        df.createOrReplaceTempView("mongo")
        self.spark.read.json(self.usercsv_txt).persist(StorageLevel.MEMORY_ONLY).cache() \
            .createOrReplaceTempView("1kuser")
        self.spark.read.load(self.oneksongs, format='json').persist(StorageLevel.MEMORY_ONLY).cache() \
            .createOrReplaceTempView("1ksong")
        self.spark.read.load(self.ratingParq, format='json').persist(StorageLevel.MEMORY_ONLY).cache() \
            .createOrReplaceTempView("temprating")
        self.spark.read.parquet(self.song_parqPATH).persist(StorageLevel.MEMORY_ONLY) \
            .createOrReplaceTempView("song")
        # "(select genreID,rating,songid,userid from temprating) union (select genreID,rating,songid,userid from mongo)"
        self.spark.sql("select genreID,rating,songid,userid from temprating") \
            .createOrReplaceTempView("rating")

    def generateParquet(self):
        # track_line = self.sc.textFile(self.train_txt)
        # songs = track_line.map(lambda l: l.split(",")) \
        #     .map(lambda p: Row(trackID=p[0], songID=p[1], artistName=p[2], songTitle=p[3]))
        #
        # tag_line = self.sc.textFile(self.tag_txt)
        # tags = tag_line.map(lambda l: l.split(",")) \
        #     .map(lambda p: Row(trackID=p[0], tagID=p[1]))
        #
        # schemaSongs = self.spark.createDataFrame(songs)
        # schemaSongs.write.parquet(self.song_parqPATH)


        # track_line = self.sc.textFile(self.train_txt)
        # songs = track_line.map(lambda l: l.split(",")) \
        #     .map(lambda p: Row(tuserID=p[0], songID=p[1], rating=float(p[2]))).take(1000000)
        #
        # schemaSongs = self.spark.createDataFrame(songs)
        # schemaSongs.createOrReplaceTempView("train")
        #
        # self.spark.sql("SELECT "
        #                "DENSE_RANK() OVER ( ORDER BY t.tuserID) as userid,s.sarkiId as songid,t.rating,s.genreID as genreID "
        #                       " FROM song as s "
        #                       "   INNER JOIN train as t ON "
        #                       "s.songID=t.songID").write.save(self.base_txt + "rating.json", format='json')
        return "ok"

        # track_line = self.sc.textFile(self.base_txt + "userid-timestamp-artid-artname-traid-traname.tsv")
        # songs = track_line.map(lambda l: l.split("\t")) \
        #     .map(lambda p: Row(user=str(p[0]), artname=str(p[3]), traname=str(p[5]))) \
        #     .take(1000000)

        # Infer the schema, and register the DataFrame as a table.

        #         track_line = self.sc.textFile(self.usercsv_txt)
        #         songs = track_line.map(lambda l: l.split(",")) \
        #             .map(lambda p: Row(userid=str(p[0]), gender=str(p[1]),age=str(p[2]), country=str(p[3])))
        #
        #         schemaSongs = self.spark.createDataFrame(songs)
        #         schemaSongs.show()
        #         schemaSongs.write.save(self.base_txt + "users.json", format='json')


        track_line = self.sc.textFile(self.usercsv_txt)
        songs = track_line.map(lambda l: l.split(",")) \
            .map(lambda p: Row(userid=str(p[0]), gender=str(p[1]), age=str(p[2]), country=str(p[3])))

        schemaSongs = self.spark.createDataFrame(songs)
        schemaSongs.show()
        schemaSongs.write.save(self.base_txt + "users.json", format='json')
