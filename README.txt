                                                                                                                                               
                                                                                                                                               
        CCCCCCCCCCCCCIIIIIIIIIIPPPPPPPPPPPPPPPPP                WWWWWWWW                           WWWWWWWW                                    
     CCC::::::::::::CI::::::::IP::::::::::::::::P               W::::::W                           W::::::W                                    
   CC:::::::::::::::CI::::::::IP::::::PPPPPP:::::P              W::::::W                           W::::::W                                    
  C:::::CCCCCCCC::::CII::::::IIPP:::::P     P:::::P             W::::::W                           W::::::W                                    
 C:::::C       CCCCCC  I::::I    P::::P     P:::::P  ooooooooooo W:::::W           WWWWW           W:::::W eeeeeeeeeeee    rrrrr   rrrrrrrrr   
C:::::C                I::::I    P::::P     P:::::Poo:::::::::::ooW:::::W         W:::::W         W:::::Wee::::::::::::ee  r::::rrr:::::::::r  
C:::::C                I::::I    P::::PPPPPP:::::Po:::::::::::::::oW:::::W       W:::::::W       W:::::We::::::eeeee:::::eer:::::::::::::::::r 
C:::::C                I::::I    P:::::::::::::PP o:::::ooooo:::::o W:::::W     W:::::::::W     W:::::We::::::e     e:::::err::::::rrrrr::::::r
C:::::C                I::::I    P::::PPPPPPPPP   o::::o     o::::o  W:::::W   W:::::W:::::W   W:::::W e:::::::eeeee::::::e r:::::r     r:::::r
C:::::C                I::::I    P::::P           o::::o     o::::o   W:::::W W:::::W W:::::W W:::::W  e:::::::::::::::::e  r:::::r     rrrrrrr
C:::::C                I::::I    P::::P           o::::o     o::::o    W:::::W:::::W   W:::::W:::::W   e::::::eeeeeeeeeee   r:::::r            
 C:::::C       CCCCCC  I::::I    P::::P           o::::o     o::::o     W:::::::::W     W:::::::::W    e:::::::e            r:::::r            
  C:::::CCCCCCCC::::CII::::::IIPP::::::PP         o:::::ooooo:::::o      W:::::::W       W:::::::W     e::::::::e           r:::::r            
   CC:::::::::::::::CI::::::::IP::::::::P         o:::::::::::::::o       W:::::W         W:::::W       e::::::::eeeeeeee   r:::::r            
     CCC::::::::::::CI::::::::IP::::::::P          oo:::::::::::oo         W:::W           W:::W         ee:::::::::::::e   r:::::r            
        CCCCCCCCCCCCCIIIIIIIIIIPPPPPPPPPP            ooooooooooo            WWW             WWW            eeeeeeeeeeeeee   rrrrrrr   V.1.0                          

                         
                         


                                                                                                                                               
  _____                               _           _     _                         _                                    _                          
 |  __ \                             (_)         | |   (_)                       | |                                  | |                         
 | |  | |   ___   ___    ___   _ __   _   _ __   | |_   _    ___    _ __       __| |  _   _      ___    ___    _ __   | |_    ___   _ __    _   _ 
 | |  | |  / _ \ / __|  / __| | '__| | | | '_ \  | __| | |  / _ \  | '_ \     / _` | | | | |    / __|  / _ \  | '_ \  | __|  / _ \ | '_ \  | | | |
 | |__| | |  __/ \__ \ | (__  | |    | | | |_) | | |_  | | | (_) | | | | |   | (_| | | |_| |   | (__  | (_) | | | | | | |_  |  __/ | | | | | |_| |
 |_____/   \___| |___/  \___| |_|    |_| | .__/   \__| |_|  \___/  |_| |_|    \__,_|  \__,_|    \___|  \___/  |_| |_|  \__|  \___| |_| |_|  \__,_|
                                         | |                                                                                                      
                                         |_|                                                                                                                                                                                                                                                     

Le fichier CIPoWer.py contient le code dans son entièreté.

Le dossier Data contient toutes les images, les documents et les fichiers .csv sauvegardés utilisé dans le programme.

Le script CIPoWer_depedencies_install.cmd est un script qui permet d'installer automatiquement toutes les
dépendances nécessaires au programme. Ce script fonctionne sur Windows mais n'a pas été testé sur d'autres 
OS (Linux, Mac).


  ____                                                                       
 |  _ \                                                                      
 | |_) |  _   _    __ _   ___      ___    ___    _ __    _ __    _   _   ___ 
 |  _ <  | | | |  / _` | / __|    / __|  / _ \  | '_ \  | '_ \  | | | | / __|
 | |_) | | |_| | | (_| | \__ \   | (__  | (_) | | | | | | | | | | |_| | \__ \
 |____/   \__,_|  \__, | |___/    \___|  \___/  |_| |_| |_| |_|  \__,_| |___/
                   __/ |                                                     
                  |___/                                                      

Le programme contient certains bugs pouvant gêner son utilisation :

Plotter une roche plutonique en premier a tendance à figer la zone du diagramme, quelque soit le type
de roche plottée après (même si ceci est plus apparent avec les roches volcaniques). Il faut alors redémarrer le programme.

Il se peut qu'une erreur de calcul du style "division par 0" arrive pour certaines normes. Il n'y a pas de solution à ceci pour l'instant.

Cocher un des boutons Volcanique ou Plutonique puis déséléctionner les deux n'empèche pas le programme de se lancer : celui-ci
sauvegarderas le dernier choix enregistré par l'utilisateur.