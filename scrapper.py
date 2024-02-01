class Scrapper:
    target_url = 'http://books.toscrape.com/' 
    
    
    def __init__(self, other_data):
        self.data = []
        self.other_data = other_data
        
    