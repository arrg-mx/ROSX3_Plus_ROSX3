# OMNI_DOFBOT
Repositorio relacionado con la implementacion de un robot movil manipulador omnidireccional en ros2, el reposiorio incluye 6 paquetes distintos los cuales 
describen y muestran al robot de manera independiente y como uno solo.

## omni_description
Este paquete contiene los elementos necesarios para mostrar la descripcion del robot en rviz, así como los controladores para su uso en gazebo.

Para visualizar el robot, se puede utilizar el archivo omni_display_launch.xml, el cual cargara el robot con sus elementos base en rviz.

En la carpeta config se encuentra el archivo de definicion de los controladores del robot omnidireccional: omni_velocitu_controller.yaml

En la carpeta meshes se pueden observar las mallas de la estructura del robot, así como las mallas de los sensores.

Dentro de la carpeta URDF se tienen los diversos archivos urdf que conforman al robot, ya sean sensores o archivos de configuracion de gazebo.
Dentro de esta, se encuentra el archivo omni_velocity_controller.xacro, el cual se encarga de juntar estos archivos y generar un urdf de la descripcion
completa del robot.
