from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Set up each test"""
        # define self.client here instead of in each method
        # check with krunal why this terminology was chosen
        # why do I have to define self.client before each test? Why not just client?

        self.client = app.test_client()
        # Make Flask errors be real errors, not HTML pages with error info
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client:
            response = self.client.get('/')
            # can also do something like this:
                        # resp = client.get('/')
                        # html = resp.get_data(as_text=True)
                        # self.assertEqual(resp.status_code, 200)
                        # self.assertIn('<h1>Color Form</h1>', html)
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'<p>High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)
            self.assertEqual(response.status_code, 200)
            html = response.get_data(as_text=True)
            self.assertIn('<table class="board">', html)

    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session"""
        # will need to create a board in session to compare sample word in 
        # get access to session
        with self.client as client:
            # create sample session transaction as sess
            with client.session_transaction() as sess:
                # define sample session board in sess
                sess['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        # create sample response - below is a get response
        # for example if you wanted to test a post response it would look like this:
            # res = client.post('/taxes', data={'income': '1000})
            # html = res.get_data(as_text=True)
            # self.assertEqual(res.status_code, 200)
            # self.assertIn('<h3>You owe $150 </h3>', html)
            # always separate web interface tests from logic tests
                # ex: separate test_submit_taxes from test_calc_taxes
                # would theoretically test web interface 1x or 2x, and logic every way
        # create sample get response below:
        # pings check-word route which returns json object
        response = self.client.get('/check-word?word=cat')
        # server responds with JSON object with key of result
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is in the dictionary"""
        self.client.get('/')
        response = self.client.get('/check-word?word=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')
        self.client.get('/')
        response = self.client.get('/check-word?word=nun')
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_non_english_word(self):
        """Test if word is on the board"""

        self.client.get('/')
        response = self.client.get(
            '/check-word?word=fsjdakfkldsfjdslkfjdlksf')
        self.assertEqual(response.json['result'], 'not-word')
        self.client.get('/')
        response = self.client.get('/check-word?word=nunchuckettes')
        self.assertEqual(response.json['result'], 'not-word')

    def test_boggle_dictionary_valid_words(self):
        """test boggle dictionary for valid words"""
        # Krunal - why does error below give a huge print out of dictionary?
        b = Boggle()
        self.assertIn('apple', b.words)
        self.assertIn('banana', b.words)
        self.assertIn('arms', b.words)

    def test_boggle_dictionary_invalid_words(self):
        """test boggle dictionary for invalid words"""
        b = Boggle()
        self.assertNotIn('appleeee', b.words)
        self.assertNotIn('bananahats', b.words)
        self.assertNotIn('banana-arms', b.words)


# Further tests:
# test board height/width
# test correct high score calculation
# test final score calculation with session 
