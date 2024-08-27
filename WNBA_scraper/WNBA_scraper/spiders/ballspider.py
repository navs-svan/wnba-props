import scrapy


class BallspiderSpider(scrapy.Spider):
    name = "ballspider"
    allowed_domains = ["www.basketball-reference.com"]
    start_urls = ["https://www.basketball-reference.com/wnba/years/2024_games.html"]

    def parse(self, response):
        rows = response.css('table#schedule tbody tr')
        for row in rows[0]:
            boxscore_url = row.css('[data-stat="box_score_text"] a::attr(href)').get()
            # boxscore_url = "www.basketball-reference.com" + relative_url
            game_data = {
                'date': row.css('[data-stat="date_game"]::text').get(),
                'away_team' : row.css('[data-stat="visitor_team_name"] a::text').get(),
                'away_score': row.css('[data-stat="visitor_pts"]::text').get(),
                'home_team': row.css('[data-stat="home_team_name"] a::text').get(),
                'home_score': row.css('[data-stat="home_pts"]::text').get()
            }

            yield response.follow(boxscore_url, callback=self.parse_boxscore, cb_kwargs=game_data)

        

    def parse_boxscore(self, response, **details):
        print(details)
        


    