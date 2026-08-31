from rich import print
from rich.table import Table

import database
from remote_control import RemoteControl


def main():
    channels = database.get_channels()

    if not channels:
        print("[red]No channels found in database.[/]")
        return

    remote_control = RemoteControl(channels)

    while True:
        remote_control.display_tv()

        command = input(
            f"\nCH({remote_control.current_channel}) "
            f"<> - VOL({remote_control.current_volume}) +- "
        ).strip()

        if command == "0":
            break

        elif command.lower() == "h":
            show_history()

        elif command.lower() == "s":
            show_statistics()

        elif command == "@":
            remote_control.power()

            action = (
                "power_on"
                if remote_control.is_on
                else "power_off"
            )

            channel = remote_control.get_current_channel()

            database.register_history(
                channel["id"],
                action
            )

        elif command == ">":
            old_channel = remote_control.current_channel

            remote_control.next_channel()

            if old_channel != remote_control.current_channel:
                channel = remote_control.get_current_channel()

                database.register_history(
                    channel["id"],
                    "channel_change"
                )

        elif command == "<":
            old_channel = remote_control.current_channel

            remote_control.previous_channel()

            if old_channel != remote_control.current_channel:
                channel = remote_control.get_current_channel()

                database.register_history(
                    channel["id"],
                    "channel_change"
                )

        elif command == "+":
            old_volume = remote_control.current_volume

            remote_control.increase_volume()

            if old_volume != remote_control.current_volume:
                channel = remote_control.get_current_channel()

                database.register_history(
                    channel["id"],
                    "volume_increase"
                )

        elif command == "-":
            old_volume = remote_control.current_volume

            remote_control.decrease_volume()

            if old_volume != remote_control.current_volume:
                channel = remote_control.get_current_channel()

                database.register_history(
                    channel["id"],
                    "volume_decrease"
                )

        else:
            print("[yellow]Unknown command.[/]")


def show_history():
    history = database.get_history()

    if not history:
        print("[yellow]No history available.[/]")
        return

    table = Table(title="REMOTE CONTROL HISTORY")

    table.add_column("Channel")
    table.add_column("Name")
    table.add_column("Action")
    table.add_column("Date")

    for item in history:
        table.add_row(
            str(item["channel_number"]),
            item["name"],
            item["action"],
            str(item["created_at"])
        )

    print(table)


def show_statistics():
    statistics = database.get_statistics()
    summary = database.get_summary_statistics()

    print(
        f"\n[bold]Channel changes:[/] "
        f"{summary['channel_changes']}"
    )

    print(
        f"[bold]Volume changes:[/] "
        f"{summary['volume_changes']}"
    )

    print(
        f"[bold]Power actions:[/] "
        f"{summary['power_actions']}\n"
    )

    table = Table(title="CHANNEL STATISTICS")

    table.add_column("Channel")
    table.add_column("Name")
    table.add_column("Selections", justify="right")

    for item in statistics:
        table.add_row(
            str(item["channel_number"]),
            item["name"],
            str(item["times_selected"])
        )

    print(table)


if __name__ == "__main__":
    main()