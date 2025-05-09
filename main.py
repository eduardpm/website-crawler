SUPPORTED_WEBSITES = ["coolblue", "emag", "alternate"]

if __name__ == "__main__":
    while True:
        choice = (
            input(
                f'Enter the website you want to crawl ({",".join(SUPPORTED_WEBSITES)}) or "exit" to stop: '
            )
            .strip()
            .lower()
        )

        match choice:
            case "coolblue":
                from coolblue.crawler import COOLBLUE_CRAWLER

                COOLBLUE_CRAWLER.crawl_all()
                exit(0)
            case "emag":
                from emag.crawler import EMAG_CRAWLER

                EMAG_CRAWLER.crawl_all()
                exit(0)
            case "alternate":
                from alternate.crawler import ALTERNATE_CRAWLER

                ALTERNATE_CRAWLER.crawl_all()
                exit(0)
            case "exit":
                print("Exiting the program.")
                exit(0)
            case _:
                print(f"Website {choice} is not supported.")
                continue
