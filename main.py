from gui import *

'''
If you don't understand what does it mean and why watch:
https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab
'''

pygame.init()

# init screen
sc = pygame.display.set_mode(size)
sc.fill(WHITE)
pygame.display.set_caption('Linear Algebra Viewer')

clock = pygame.time.Clock()


def main():
    run = True
    # information about vector: (type of vector, position in list) or None
    grabbed_vector = None
    while run:
        # fps in config
        clock.tick(fps)
        # checking events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # check is any vector grabbed
            if event.type == pygame.MOUSEBUTTONDOWN:
                # get: (type of vector, position in list) or None
                vector = transformed_grid.check_grabbing(pygame.mouse.get_pos())
                grabbed_vector = vector
                if vector:
                    # put vector in buffer to change it via tab
                    transformed_grid.prev_vector = transformed_grid.prev_vector if vector[0] == 'basis' else vector
            # put grabbed vector, it is still in buffer
            if event.type == pygame.MOUSEBUTTONUP:
                grabbed_vector = None
        # move grabbed vector
        if grabbed_vector:
            # check vector type, then change coords
            if grabbed_vector[0] == 'basis':
                # change transformed coords
                transformed_grid.basis_vectors[grabbed_vector[1]].change_cords(pygame.mouse.get_pos())
                # apply transformation to whole surface
                transformed_grid.transform()
            if grabbed_vector[0] == 'common':
                # transformed coords(t) determined by mouse position
                transformed_grid.vectors[grabbed_vector[1]].change_cords(pygame.mouse.get_pos())
                # x = coords relatively to basis vectors
                # M = such matrix of linear transformation that t = Mx
                # Therefore, (M^(-1))t = (M^(-1))Mx = x,
                # where M^(-1) - inverted matrix M
                transformed_grid.vectors[grabbed_vector[1]].coords = np.linalg.inv(transformed_grid.get_matrix()).dot(
                    transformed_grid.vectors[grabbed_vector[1]].transformed)
            update_information(main_window)
        # show all in screen
        sc.fill(WHITE)
        main_grid.draw_object(sc)
        transformed_grid.draw_object(sc)
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    # init and show information tab
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    main()
    sys.exit()
