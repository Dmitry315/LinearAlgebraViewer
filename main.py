from gui import *

pygame.init()

sc = pygame.display.set_mode(size)
sc.fill(WHITE)
clock = pygame.time.Clock()
pygame.display.set_caption('Linear Algebra Viewer')


def main():
    run = True
    grabbed_vector = None
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # check is any vector grabbed
            if event.type == pygame.MOUSEBUTTONDOWN:
                vector = transformed_grid.check_grabbing(pygame.mouse.get_pos())
                grabbed_vector = vector
                if vector:
                    transformed_grid.prev_vector = transformed_grid.prev_vector if vector[0] == 'basis' else vector
            # put grabbed vector
            if event.type == pygame.MOUSEBUTTONUP:
                grabbed_vector = None
        # move grabbed vector
        if grabbed_vector:
            # check vector type, then change cords
            if grabbed_vector[0] == 'basis':
                transformed_grid.basis_vectors[grabbed_vector[1]].change_cords(pygame.mouse.get_pos())
                transformed_grid.transform()
                # update information
                main_window.matrix00.setText(str(round(transformed_grid.basis_vectors[0].transformed[0], 3)))
                main_window.matrix10.setText(str(round(transformed_grid.basis_vectors[0].transformed[1], 3)))
                main_window.matrix01.setText(str(round(transformed_grid.basis_vectors[1].transformed[0], 3)))
                main_window.matrix11.setText(str(round(transformed_grid.basis_vectors[1].transformed[1], 3)))
            if grabbed_vector[0] == 'common':
                transformed_grid.vectors[grabbed_vector[1]].change_cords(pygame.mouse.get_pos())
                transformed_grid.vectors[grabbed_vector[1]].cords = np.linalg.inv(transformed_grid.get_matrix()).dot(
                    transformed_grid.vectors[grabbed_vector[1]].transformed)
            update_information(main_window)
        sc.fill(WHITE)
        main_grid.draw_object(sc)
        transformed_grid.draw_object(sc)
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    main()
    sys.exit()
