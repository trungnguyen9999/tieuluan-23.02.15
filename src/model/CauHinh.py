class CauHinh:
    def __init__(self, ch_id, gv_id, value):
        self.ch_id = ch_id
        self.gv_id = gv_id
        self.value = value

    @staticmethod
    def create_table(cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS public.cauhinh
            (
                ch_id integer NOT NULL DEFAULT nextval('cauhinh_ch_id_seq'::regclass),
                gv_id integer NOT NULL,
                value text COLLATE pg_catalog."default" NOT NULL,
                CONSTRAINT cauhinh_pkey PRIMARY KEY (ch_id)
            )
        """)

    def save(self, cursor):
        cursor.execute("""
            INSERT INTO public.cauhinh (gv_id, value) VALUES (%s, %s)
        """, (self.gv_id, self.value))
        cursor.connection.commit()

    @staticmethod
    def load_all(cursor):
        cursor.execute("""
            SELECT * FROM public.cauhinh
        """)
        rows = cursor.fetchall()
        return [CauHinh(*row) for row in rows]
