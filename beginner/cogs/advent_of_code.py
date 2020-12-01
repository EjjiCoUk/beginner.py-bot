from beginner.colors import BLUE
from beginner.cog import Cog, commands
from beginner.scheduler import schedule
from beginner.tags import tag
from datetime import datetime, timedelta
import discord
import discord.ext.commands
import dateutil.tz


class AdventOfCode(Cog):
    @property
    def now(self):
        return datetime.now(dateutil.tz.gettz("America/New_York")).replace(hour=0, minute=0, second=0, microsecond=0)

    @property
    def christmas(self):
        return datetime(2020, 12, 25, 0, 0, 0, tzinfo=dateutil.tz.gettz("America/New_York"))

    @property
    def days_till_christmas(self):
        return (self.christmas - self.now).days

    async def ready(self):
        if self.now < self.christmas + timedelta(days=1):
            print("🎄🎅☃️ 🤶🎄🤶☃️ 🎅🎄")
            print(self.days_till_christmas, "days until Christmas!!!")
            self.schedule_next_challenge_announcement()

    def schedule_next_challenge_announcement(self):
        if self.days_till_christmas:
            schedule(
                "beginnerpy-advent-of-code-2020",
                self.now + timedelta(days=1, minutes=1),
                self.send_daily_link,
                no_duplication=True
            )

    @tag("schedule", "advent-of-code-announcement")
    async def send_daily_link(self):
        channel = self.get_channel("🎅announcements")
        show_off = self.get_channel("⛄discussion")
        help_1 = self.get_channel("🤶advent-of-code-help")
        help_2 = self.get_channel("🎄advent-of-code-help")
        suffixes = {1: "st", 21: "st", 2: "nd", 22: "nd", 3: "rd", 23: "rd"}
        await channel.send(
            embed=discord.Embed(
                description=(
                    f"Here's the [{self.now.day}{suffixes.get(self.now.day, 'th')} challenge]"
                    f"(https://adventofcode.com/2020/day/{self.now.day})!!!\n\n"
                    f"Show off (spoiler tag please) & discuss in {show_off.mention}!!! Get help in {help_1.mention} or "
                    f"{help_2.mention}.\n\n"
                    f"**Good luck!!!**"
                ),
                title=(
                    f"TESTING🎄 {self.days_till_christmas} Days Until Christmas 🎄"
                    if self.days_till_christmas else
                    "🎄🎅☃️  MERRY CHRISTMAS ☃️ 🎅🎄"
                ),
                color=BLUE,
            )
        )

        self.schedule_next_challenge_announcement()


def setup(client):
    client.add_cog(AdventOfCode(client))
