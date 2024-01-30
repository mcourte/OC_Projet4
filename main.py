from controllers import main_controller

# Programme principal
if __name__ == '__main__':

    try:
        main_controller = main_controller.MainController()
        main_controller.run()
    except KeyboardInterrupt:
        print("Arret du programme")
