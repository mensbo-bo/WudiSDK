
import asyncio
import asyncpg
import aiocache

from . import config



#------------------------------------------------------------
# Class untuk membuat table yang diperlukan untuk server
# WudiGraph
#------------------------------------------------------------
class WMCreateTable:
    async def WCreate_table_users(self, conn):
        await conn.execute('''
        CREATA TABLE IF NOT EXISTS tbl_users(
            id_user SERIAL PRIMARY KEY,
            username VARCHAR(200),
            password VARCHAR(255),
            email VARCHAR(100),
            session VARCHAR(100),
            free_premium VARCHAR(100) DEFAULT 'free'
        )
        ''')

    async def WCreate_table_admin(self, conn):
        await conn.execute('''
        CREATE TABLE IF NOT EXISTS tbl_admin(
            id_admin SERIAL PRIMARY KEY,
            username VARCHAR(100),
            password VARCHAR(100),
            email VARCHAR(100),
            session VARCHAR(100),
            level_access VARCHAR(50) DEFAULT 'admin'
        )
        ''')
    async def WCreate_table_usertoken(self, conn):
        await conn.execute('''
        CREATE TABLE IF NOT EXISTS tbl_user_server_token(
        user_server_token VARCHAR(100) UNIQUE,
        waktu_dibuat DATE,
        waktu_berakhir DATE,
        FOREIGN KEY (users_id) REFERENCES tbl_users(id_user)
        )
        ''')

    async def WCreate_table_temptoken(self, conn):
        await conn.execute('''
        CREATE TABLE IF NOT EXIST tbl_temp_token(
            FOREIGN KEY (user_token_id) RENFERENCES tbl_user_server_token(user_server_token),
            temp_client_token VARCHAR(100)        
        )
        ''')


#-------------------------------------------------------------
# Class untuk melakukan CREATE, READ, UPDATE dan DELETE dalam
# database postgres
#-------------------------------------------------------------
class WMCRUDServerUsers:
    def __init__(self) -> None:
        self.conn = asyncio.run(self.WConnect_db())

    async def WConnect_db(self):
        return await asyncpg.connect(
            **config.DATABASE['postgresql']
        )
    
    #-------------------------------------------------------
    # Insert Data
    #-------------------------------------------------------
    
    async def WInsert_user(self, username, password, email, session, tier):
        query = """
        INSERT INTO tbl_user (username, password, email, session, free_premium)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id_user;
        """
        return await self.conn.fetchval(query, username, password, email, session, tier)
    
    async def WInsert_admin(self, username, password, email, session, access):
        query = """
        INSERT INTO tbl_admin (username, password, email, session, level_access)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id_admin;
        """
        return await self.conn.fetchval(query, username, password, email, session, access)
    
    async def WInsert_user_token(self, id_user, token, waktu_dibuat, waktu_berakhir):
        query = """
        INSERT INTO tbl_user_server_token 
        (id_user, user_server_token, waktu_dibuat, waktu_berakhir)
        VALUES ($1, $2, $3, $4);
        """
        await self.conn.execute(query, id_user, token, waktu_dibuat, waktu_berakhir)

    async def WInsert_temptoken(self, user_server_token, temp_token):
        query ='''
        INSERT INTO tbl_temp_token(user_server_token, temp_client_token)
        VALUES ($1, $2)
        '''
        await self.conn.execute(query, user_server_token, temp_token)

    #-------------------------------------------------------------------
    # SELECT DATA
    #-------------------------------------------------------------------
    async def WGet_user(self, username):
        query = """
        SELECT * FROM tbl_user
        WHERE username = $1;
        """
        return await self.conn.fetchrow(query, username)
    
    async def WGet_full_token_data(self, id_user):
        query = """
        SELECT 
            u.username,
            ust.user_server_token,
            ust.waktu_dibuat,
            ust.waktu_berakhir,
            tt.temp_client_token
        FROM tbl_user u
        JOIN tbl_user_server_token ust 
            ON u.id_user = ust.id_user
        LEFT JOIN tbl_temp_token tt 
            ON ust.user_server_token = tt.user_server_token
        WHERE u.id_user = $1;
        """
        return await self.conn.fetch(query, id_user)
    
    # ----------------------------------------------------------
    # UPDATE 
    # ----------------------------------------------------------

    async def WUpdate_user_session(self, id_user, new_session):
        query = """
        UPDATE tbl_user
        SET session = $1
        WHERE id_user = $2;
        """
        await self.conn.execute(query, new_session, id_user)

    # -----------------------------------------------------------
    # DELETE
    # -----------------------------------------------------------
    async def WDelete_expired_tokens(self, user_token_id):
        """ Menghapus temporary token terlebih dahulu dari 
        tbl_temp_token agar data benar-benar di hapus
        """
        query = '''
        DELETE FROM tbl_temp_token
        WHERE user_token_id = $1
        '''
        await self.conn.excute(query, user_token_id)

        query = """
        DELETE FROM tbl_user_server_token
        WHERE waktu_berakhir < NOW();
        """
        await self.conn.execute(query)

