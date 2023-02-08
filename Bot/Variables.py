import os

discordApiToken = "NjMwMzMyNDAzODY0NTY3ODA4.GHl_9-.CBuEZoqP0_sz6xST-euA1VJVFNkzt3ZqXgYSL4"
clashOfClansHeaders = {
    "Accept": "application/json",
    "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjEwNjQyN2E0LWIzNmUtNGFkNi1hZTYwLWQzOTUyNDY3N2I0MiIsImlhdCI6MTY2NzgzMDA5Miwic3ViIjoiZGV2ZWxvcGVyL2VhOWNkOWYwLTQwMDMtZjI1My05MmZkLWI1OTE3ZmNiM2FkOCIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjEzOS4xNjUuMzEuMTQiLCIxMzkuMTY1LjMxLjE1IiwiODEuMjQ0LjIxOC4xNTEiLCIxMDkuMTMwLjczLjE2OCJdLCJ0eXBlIjoiY2xpZW50In1dfQ.r8_38CAKrLSMDU3o0tCvuiu-YS7EzpIwMv6qNyDnrf_PhaC1qL0rknHhiSjklBAYtxfCA2e5oZ0rho74PezHNg"
}
messageOnGuildJoin = "Hello there!"
discordServer = "no discord server yet"
log = "HeadhunterBot.log"
current_working_directory = os.getcwd()
path = current_working_directory[:current_working_directory.find("HeadhunterBot") + 13]
database = "/".join((path, "Database", "HeadhunterBot.db"))
wars_per_page = 10
embed_color = 0x513B54
