# ROSX3_Plus_ROSX3
Repositorio relacionados con la implementación de los robots móviles ROSX3 Plus y ROSX3.

##URDF
En la carpeta urdf se encuentran 2 archivos que contienen la descripción del robot. El archivo yahboomcar_X3 corresponde al robot ROSX3, mientras que full_yahboomcar_X3 corresponde al robot ROSX3 Plus.
En este segundo archvivo, se definen los siguientes aspectos:

-Materiales: son aquellos que se utilizarán para mostrar el robot en Gazebo
-Eslabones: se define el origen del eslabón, la ruta para la malla que describe su geometría, intercia, masa y color. 
-Juntas: se definen los eslabones que están siendo unidos y el origen.
-Transmisiones: estos elementos hacen referencias a las juntas y actuadores que serán utilizados para controlar el robot en Gazebo una vez que se implemente el plugin correspondiente.
-Plugin: se añade el plugin para controlar el robot. Con la implementación actual aún no es posible esto. En el caso del robot ROSX3 se utiliza un plugin para bases omnidireccionales; sin embargo, se especula que éste se encuentra desactualizado. En el caso del robot ROSX3 Plus se incluyó el plugin "control" que se encuentra en libgazebo_ros_control.so

Todo lo anterior se define para 3 elementos básicos del robot:
-Brazo robótico y gripper.
-Base móvil.
-Sensores.

##Launch
En la carpeta launch se encuentran 2 archivos, que permiten visualizar en RViz y en Gazebo al robot móvil ROSX3 Plus y ROSX3. Display.launch corresponde al primer robot y full_robot_display al segundo. Como parámetro se incluye en ambos launch la ruta con la descripción del robot, la cual está definida en los archivos urdf mencionados con anterioridad.
Se inicializa el nodo correspondiente al publicador de estados del robot, rviz y Gazebo. En el caso del robot ROSX3 Plus, el bloque de código correspondiente a Gazebo se encuentra comentado, puesto que ocasionaba problemas en RViz y como resultado el brazo robótico no era incluido. El nodo joint_state_publisher_gui permite inicializar una interfaz gráfica a través de la cual pueden enviarse posiciones al robot. 
Finalmente, se encuentra incluido también un nodo asociado al controlador del robot. Como argumentos se pasan los nombres de las transmisiones definidas en el urdf. 
