import requests
import json


class Api(object):

    idx=0
    
    urls = ['AIzaSyDiT9c1NfoAW4vE-UeLYwwKHb9C1AkQUsY',     # aheroaa
            'AIzaSyCv0a6F-Eriy5_Yl5WMYbSSCUVxJtYHIB8',      # aheroab
            'AIzaSyDZL0MVOIzzqj7S-IEHipUWQ7Upoi2xN4w',     # meric
            'AIzaSyA24n01eJnWWHO12zXiIgFF5r9WpnyX9xQ',     # meric1
            'AIzaSyCARLjZL54gMrlUHy2liDQyQKsLuIGYqrk',     # meric2
            'AIzaSyBTLg4ilVc0sPm5RHaW0Z-3qB00GBmc1gM',     # meric3
            'AIzaSyDQOffUzpgTfgr4XKwYkeIRejW7OeFcqh4',     # meric4
            'AIzaSyDzRfPPpID7ihN4ZOQ9Ou_pvL7GlRPX7jI',     # meric5
            'AIzaSyAuThUpW8HlJyXLqMZR_YZZEF-YJK006-o',     # meric6
            'AIzaSyC9Zi-JvMz7IT88Hg0oZNdPhVl0AJKlOtQ',     # meric8
            'AIzaSyA1XwbYojAaujbzBNXhvU9__I1s1b3kgms',     # meric9
            'AIzaSyAI7GnLhUQv1yHCHtmRzOOWg8FlGEOfHrI'      # meric7
            ]

    """Google Books Api
    
    See: https://developers.google.com/books/
    """
    __BASEURL = 'https://www.googleapis.com/books/v1'

    def __init__(self):
       pass

    def _get(self, path, params=None):
        global urls,idx
        if params is None:
            params = {}
        
        # aheroaa
        #params['key'] = 'AIzaSyDiT9c1NfoAW4vE-UeLYwwKHb9C1AkQUsY'
        # aheroab
        # params['key'] = 'AIzaSyCv0a6F-Eriy5_Yl5WMYbSSCUVxJtYHIB8'
        # meric
        #params['key'] = 'AIzaSyDZL0MVOIzzqj7S-IEHipUWQ7Upoi2xN4w'
        

        # #meric1
        # params['key'] = 'AIzaSyA24n01eJnWWHO12zXiIgFF5r9WpnyX9xQ'
        # #meric2
        #params['key'] = 'AIzaSyCARLjZL54gMrlUHy2liDQyQKsLuIGYqrk'
        # meric3
        #params['key'] = 'AIzaSyBTLg4ilVc0sPm5RHaW0Z-3qB00GBmc1gM'
        # #meric4
        # params['key'] = 'AIzaSyDQOffUzpgTfgr4XKwYkeIRejW7OeFcqh4'
        # #meric5
        # params['key'] = 'AIzaSyDzRfPPpID7ihN4ZOQ9Ou_pvL7GlRPX7jI'
        #meric6
        #params['key'] = 'AIzaSyAuThUpW8HlJyXLqMZR_YZZEF-YJK006-o'
        # #meric7
        # params['key'] = 'AIzaSyAI7GnLhUQv1yHCHtmRzOOWg8FlGEOfHrI'
        # #meric8
        #params['key'] = 'AIzaSyC9Zi-JvMz7IT88Hg0oZNdPhVl0AJKlOtQ'
        # # meric9
        # params['key'] = 'AIzaSyA1XwbYojAaujbzBNXhvU9__I1s1b3kgms'
        
        params['key'] = Api.urls[Api.idx]

        resp = requests.get(self.__BASEURL+path, params=params, proxies={
            "http": "socks5://127.0.0.1:1080",
            'https': 'socks5://127.0.0.1:1080'
        })
        if resp.status_code == 200:
            return json.loads(resp.content)

        return resp

    def get(self, volumeId, **kwargs):
        """Retrieves a Volume resource based on ID

        volumeId -- ID of volume to retrieve.

        Optional Parameters:

        partner --  Brand results for partner ID.
        
        projection -- Restrict information returned to a set of selected fields. 

                    Acceptable values are:
                    "full" - Includes all volume data.
                    "lite" - Includes a subset of fields in volumeInfo and accessInfo.
        
        source --   String to identify the originator of this request.

        See: https://developers.google.com/books/docs/v1/reference/volumes/get
        """
        path = '/volumes/'+volumeId
        params = dict()
        for p in 'partner projection source'.split():
            if p in kwargs:
                params[p] = kwargs[p]

        return self._get(path)

    def list(self, q, **kwargs):
        """Performs a book search.

        q -- Full-text search query string.
            
            There are special keywords you can specify in the search terms to
            search in particular fields, such as:

            intitle: Returns results where the text following this keyword is
                    found in the title.
            inauthor: Returns results where the text following this keyword is
                    found in the author.
            inpublisher: Returns results where the text following this keyword
                    is found in the publisher.
            subject: Returns results where the text following this keyword is
                    listed in the category list of the volume.
            isbn:   Returns results where the text following this keyword is the
                    ISBN number.
            lccn:   Returns results where the text following this keyword is the
                    Library of Congress Control Number.
            oclc:   Returns results where the text following this keyword is the
                    Online Computer Library Center number.

        Optional Parameters:

        download -- Restrict to volumes by download availability. 

                    Acceptable values are:
                    "epub" - All volumes with epub.

        filter --   Filter search results. 

                    Acceptable values are:
                    "ebooks" - All Google eBooks.
                    "free-ebooks" - Google eBook with full volume text viewability.
                    "full" - Public can view entire volume text.
                    "paid-ebooks" - Google eBook with a price.
                    "partial" - Public able to see parts of text.

        langRestrict -- Restrict results to books with this language code.

        libraryRestrict	-- Restrict search to this user's library. 

                    Acceptable values are:
                    "my-library" - Restrict to the user's library, any shelf.
                    "no-restrict" - Do not restrict based on user's library.

        maxResults -- Maximum number of results to return. Acceptable values are 0 to 40, inclusive.

        orderBy	 -- Sort search results. 

                    Acceptable values are:
                    "newest" - Most recently published.
                    "relevance" - Relevance to search terms.

        partner	--  Restrict and brand results for partner ID.

        printType -- Restrict to books or magazines. 

                    Acceptable values are:
                    "all" - All volume content types.
                    "books" - Just books.
                    "magazines" - Just magazines.

        projection -- Restrict information returned to a set of selected fields. 

                    Acceptable values are:
                    "full" - Includes all volume data.
                    "lite" - Includes a subset of fields in volumeInfo and accessInfo.
        
        showPreorders -- Set to true to show books available for preorder. Defaults to false.

        source --  String to identify the originator of this request.

        startIndex -- Index of the first result to return (starts at 0)

        See: https://developers.google.com/books/docs/v1/reference/volumes/list
        """
        path = '/volumes'
        params = dict(q=q)
        for p in 'download filter langRestrict libraryRestrict maxResults orderBy partner printType projection showPreorders source startIndex'.split():
            if p in kwargs:
                params[p] = kwargs[p]

        return self._get(path, params)
