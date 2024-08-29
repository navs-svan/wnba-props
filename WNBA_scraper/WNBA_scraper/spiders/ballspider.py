import scrapy
from WNBA_scraper.items import PlayerProps


class BallspiderSpider(scrapy.Spider):
    name = "ballspider"
    allowed_domains = ["www.basketball-reference.com"]
    start_urls = ["https://www.basketball-reference.com/wnba/years/2024_games.html"]

    def parse(self, response):
        rows = response.css("table#schedule tbody tr")
        for row in rows:
            if boxscore_url := row.css('td:not([class*="iz"])[data-stat="box_score_text"] a::attr(href)').get():
                # boxscore_url = "www.basketball-reference.com" + relative_url
                game_data = {
                    "date": row.css('[data-stat="date_game"]::text').get(),
                    "away_team": row.css('[data-stat="visitor_team_name"] a::text').get(),
                    "home_team": row.css('[data-stat="home_team_name"] a::text').get(),
                }

                yield response.follow(
                    boxscore_url, callback=self.parse_boxscore, cb_kwargs=game_data
                )

    def parse_boxscore(self, response, date, away_team, home_team):

        abbrs = response.css(
            "div.game_summary.current table.teams.poptip tbody tr td a"
        )
        props = PlayerProps()
        home_court = (False, True)
        team = (away_team, home_team)

        for i in range(1, -2, -1):
            # away team is at abbrs[0] while home team is at abbrs[-1]
            abbr = abbrs[i].css("::text").get()
            basic_css = f'table#box-{abbr}-game-basic tbody tr:not([class*="thead"])'
            basic_players = response.css(basic_css)

            advanced_css = f'table#{abbr}-advanced tbody tr:not([class*="thead"])'
            advanced_players = response.css(advanced_css)

            for basic, advanced in zip(basic_players, advanced_players):

                props["name"] = basic.css("th a::text").get()
                props["minutes"] = basic.css('[data-stat="mp"]::text').get()
                props["field_goals"] = basic.css('[data-stat="fg"]::text').get()
                props["fg_attempts"] = basic.css('[data-stat="fga"]::text').get()
                props["fg_percent"] = basic.css('[data-stat="fg_pct"]::text').get()
                props["fg_three"] = basic.css('[data-stat="fg3"]::text').get()
                props["fg_three_attempts"] = basic.css('[data-stat="fg3a"]::text').get()
                props["fg_three_percent"] = basic.css(
                    '[data-stat="fg3_pct"]::text'
                ).get()
                props["rb_offensive"] = basic.css('[data-stat="orb"]::text').get()
                props["rb_total"] = basic.css('[data-stat="trb"]::text').get()
                props["assists"] = basic.css('[data-stat="ast"]::text').get()
                props["steals"] = basic.css('[data-stat="stl"]::text').get()
                props["blocks"] = basic.css('[data-stat="blk"]::text').get()
                props["turnovers"] = basic.css('[data-stat="tov"]::text').get()
                props["personal_fouls"] = basic.css('[data-stat="pf"]::text').get()
                props["points"] = basic.css('[data-stat="pts"]::text').get()
                props["plus_minus"] = basic.css('[data-stat="plus_minus"]::text').get()

                props["true_shoot_percent"] = advanced.css(
                    '[data-stat="ts_pct"]::text'
                ).get()
                props["efg_percent"] = advanced.css('[data-stat="efg_pct"]::text').get()
                props["three_pt_attempt"] = advanced.css(
                    '[data-stat="fg3a_per_fga_pct"]::text'
                ).get()
                props["ft_attempt"] = advanced.css(
                    '[data-stat="fta_per_fga_pct"]::text'
                ).get()
                props["rb_off_percent"] = advanced.css(
                    '[data-stat="orb_pct"]::text'
                ).get()
                props["rb_def_percent"] = advanced.css(
                    '[data-stat="drb_pct"]::text'
                ).get()
                props["rb_tot_percent"] = advanced.css(
                    '[data-stat="trb_pct"]::text'
                ).get()
                props["assist_percent"] = advanced.css(
                    '[data-stat="ast_pct"]::text'
                ).get()
                props["steal_percent"] = advanced.css(
                    '[data-stat="stl_pct"]::text'
                ).get()
                props["block_percent"] = advanced.css(
                    '[data-stat="blk_pct"]::text'
                ).get()
                props["turnover_percent"] = advanced.css(
                    '[data-stat="tov_pct"]::text'
                ).get()
                props["usage_percent"] = advanced.css(
                    '[data-stat="usg_pct"]::text'
                ).get()
                props["off_rating"] = advanced.css('[data-stat="off_rtg"]::text').get()
                props["def_rating"] = advanced.css('[data-stat="def_rtg"]::text').get()

                props["home_court"] = home_court[i]
                props["date"] = date
                props["team"] = team[i]


                yield props
