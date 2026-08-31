from rich.panel import Panel
from rich import print


class RemoteControl:
    min_volume = 1
    max_volume = 5

    def __init__(self, channels, volume=2):
        self.channels = channels
        self.current_volume = volume
        self.current_channel = channels[0]["channel_number"]
        self.is_on = False

    def power(self):
        self.is_on = not self.is_on

    def decrease_volume(self):
        if self.is_on and self.current_volume > self.min_volume:
            self.current_volume -= 1

    def increase_volume(self):
        if self.is_on and self.current_volume < self.max_volume:
            self.current_volume += 1

    def next_channel(self):
        if not self.is_on:
            return

        current_index = next(
            i for i, channel in enumerate(self.channels)
            if channel["channel_number"] == self.current_channel
        )

        next_index = (current_index + 1) % len(self.channels)

        self.current_channel = self.channels[next_index]["channel_number"]

    def previous_channel(self):
        if not self.is_on:
            return

        current_index = next(
            i for i, channel in enumerate(self.channels)
            if channel["channel_number"] == self.current_channel
        )

        previous_index = (current_index - 1) % len(self.channels)

        self.current_channel = self.channels[previous_index]["channel_number"]

    def get_current_channel(self):
        return next(
            channel for channel in self.channels
            if channel["channel_number"] == self.current_channel
        )

    def display_tv(self):
        if not self.is_on:
            print(
                "[red]:prohibited: The TV is turned off. "
                "Press @ to turn it on.[/]"
            )
            return

        current_channel = self.get_current_channel()

        content = "CHANNEL = "

        for channel in self.channels:
            number = channel["channel_number"]

            if number == self.current_channel:
                content += f"[yellow on yellow] {number}[/]"
            else:
                content += f" {number}"

        content += "\nVOLUME = "

        for volume in range(self.min_volume + 1, self.max_volume + 1):
            if volume <= self.current_volume:
                content += "[black on white]   [/]"
            else:
                content += "[blue on cyan]   [/]"

        content += (
            f"\n\n[bold]{current_channel['name']}[/]"
            f"\n{current_channel['category']}"
            f" | {current_channel['country']}"
            f" | {current_channel['language']}"
        )

        tv = Panel(content, title="[ TV ]", width=55)
        print(tv)