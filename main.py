import sys


if __name__ == "__main__":
    # print(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        # print(f"Argument {i:>6}: {arg}")
        if arg == "-startServer":
            import server.Server
            server.Server.main()
        elif arg == "-startClient":
            import client.Client
            client.Client.main()