SUPPORTED_WEBSITES = ["coolblue", "emag", "alternate"]

if __name__ == "__main__":
    while True:
        choice = input(f'Enter the website you want to crawl ({",".join(SUPPORTED_WEBSITES)}) or "exit" to stop: ').strip().lower()

        match choice:
            case "coolblue":
                from coolblue.coolblue import crawl_coolblue
                crawl_coolblue()
                exit(0)
            case "emag":
                from emag.emag import crawl_emag
                crawl_emag()
                exit(0)
            case "alternate":
                from alternate.alternate import crawl_alternate
                crawl_alternate()
                exit(0)
            case "exit":
                print("Exiting the program.")
                exit(0)
            case _:
                print(f"Website {choice} is not supported.")
                continue