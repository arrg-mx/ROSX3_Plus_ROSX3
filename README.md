# omni dofbot
## Descripción General
Este repositorio contiene la implementación de un robot manipulador móvil omnidireccional utilizando ROS2. Incluye múltiples paquetes que describen y demuestran la funcionalidad del robot tanto de manera independiente como en conjunto. El proyecto está estructurado para facilitar el desarrollo y la prueba de varios componentes del robot.

## Estructura del Repositorio
El repositorio está organizado en varios paquetes, cada uno con un propósito específico. A continuación se presenta una breve descripción de cada paquete y su contenido:

### 1. dofbot_bringup
Contiene archivos de lanzamiento y configuraciones para poner en marcha el robot dofbot.
Archivos Clave:
- **launch/dofbot_trajectory_controller.launch.py**: Archivo de lanzamiento para el controlador de trayectoria, este script lanza el dofbot en gazebo y rviz con un controlador para la trayectoria del dofbot y otro para el gripper.
- **rviz/dofbot_trajectory_rviz.rviz**: Archivo de configuración de rviz para visualizar el robot.
- **src/**: Archivos para publicar en los controladores, los scripts 'dofbot_gripper_test.py' y 'dofbot_trajectory_test.py' publican trayectorias predefinidas para el gripper y el brazo del dofbot respectivamente.
- **world/test_world.world**: Archivo de mundo para simulación en Gazebo.

### 2. dofbot_description
Proporciona la descripción del robot dofbot, incluyendo su URDF y modelos visuales.
Archivos Clave:
- **config/dofbot_trajectory_controller.yaml**: Archivo de configuración para los controladores del dofbot.
- **launch/dofbot_arm.launch.xml**: Este archivo permite lanzar el dofbot para su visualizaciion en rviz y el control de sus juntas con el 'joint_state_publisher_gui'
- **meshes/**: Contiene archivos STL para los componentes visuales del robot.
- **rviz/dofbot_arm_rviz.rviz**: Configuración de rviz para el brazo del dofbot.
- **urdf/**: Contiene archivos Xacro para generar el URDF del robot.


### 3. omni_bringup
Contiene archivos de lanzamiento y configuraciones para el robot omnidireccional.
Archivos Clave:
- **launch/simple_velocity_controller.launch.py**: Archivo de lanzamiento en gazebo y rviz para el controlador de velocidad del robot móvil.
- **rviz/omni_velocity_rviz.rviz**: Configuración de RViz para el robot Omni.
- **world/Mundo_mesa_y_cajas.world**: Archivo de mundo para simulación en Gazebo.

### 4. omni_description
Proporciona la descripción del robot Omni, incluyendo su URDF y modelos visuales.
Archivos Clave:
- **config/omni_velocity_controller.yaml**: Archivo con los parámetros de configuración del control de velocidad para el robot omnidireccional.
- **launch/omni_display.launch.xml**: Este archivo lanza una instancia en rviz para visualizar el robot omni y el joint_state_publisher_gui para controlar las juntas.
- **meshes/**: Contiene archivos STL para los componentes visuales del robot.
- **rviz/omni_rviz.rviz**: Archivo con la configuracion de rviz para su visualizacion.
- **urdf/**: Contiene archivos Xacro para generar el URDF del robot.

### 5. omni_dofbot_bringup
Contiene archivos de lanzamiento y configuraciones para el robot Omni Dofbot.
Archivos Clave:
- **launch/omni_dofbot_controller.launch.py**: Archivo de lanzamiento para el controlador del omni_dofbot, lanza los controladores para el dofbot y el movil, el robot se visualiza en rviz y gazebo con sus sensores.
- **rviz/omni_dofbot_trayectory_rviz.rviz**: Configuración de rviz para el Omni Dofbot.

### 6. omni_dofbot_description
Proporciona la descripción del robot omni_dofbot, incluyendo su URDF y modelos visuales.
Archivos Clave:
- **config/omni_dofbot_controller.yaml**: Este archivo contiene los paramentros de los controladores implementados en el omni_dofbot.
- **launch/omni_dofbot_display.launch.xml**: Archivo que lanza una instancia para la visualizacion del robot en rviz y el nodo joint_state_publisher_gui.
- **meshes/**: Contiene archivos STL para los componentes visuales del Omni Dofbot.
- **urdf/**: Contiene archivos Xacro para generar el URDF del omni_dofbot.

## ¿Cómo instalar el paquete?

### Paso 1. Agregar el repositorio:
Crea un espacio de trabajo destinado a este repositorio dentro de tu carpeta de ros, y dentro de él una carpeta src, por ejemplo:

```shell
$ mkdir -p ~/ROS2Dev/omni_dofbot/src
```

Ahora muévete a la carpeta /src e inicia git para añadir el repositorio ROSX3_Plus_ROSX3:

```shell
$ cd ~/ROS2Dev/omni_dofbot/src
```

```shell
$ git init
```

```shell
$ git remote add origin https://github.com/arrg-mx/ROSX3_Plus_ROSX3.git
```

Haz un pull para tener de manera local los archivos del repositorio:
```shell
$ git pull origin
```

Finalmente, una vez se bajen todos los archivos, cambia a la branch humble, que es la que funciona con ros2:
```shell
$ git checkout humble 
```

### Paso 2. Compilar los paquetes y hacerles un source:
Vuelve al nivel de la carpeta de /src
```shell
$ cd ..
```

Compila todos los paquetes: 
```shell
$ colcon build
```

Ahora realiza un source a la carpeta de install
```shell
$ source install/setup.bash
```

### Paso 3. Prueba los paquetes:
Por ejemplo, probemos el omni_dofbot: 
```shell
$ ros2 launch omni_dofbot_bringup omni_dofbot_controller.launch.py 
```

Una vez spawneado el robot en gazebo y rviz podemos usar los scripts de los controladores en otra terminal **no olvides volver a hacer source en esta terminal**, por ejemplo: 
```shell
$ ros2 run dofbot_bringup dofbot_trajectory_test.py 
```

## Notas
### Gazebo
Si se presentan problemas al visualizar las mallas en Gazebo:
#### Solución 1.
En caso de que tengas problemas para visualizar el robot en gazebo, puedes modificar la ruta de gazebo model path que se encuentra en los metadatos del archivo package.xml de cada paquete de description, el fragmento que debes modificar es el siguiente. Deberas hacer esto para los 3 paquetes de description.

```xml
  <export>
    <build_type>ament_cmake</build_type>
    <gazebo_ros gazebo_model_path = "ruta/del/directorio/share/del/paquete/description"/>
  </export>
```

#### Solución 2.
Copiar directamente las 3 carpetas de description al directorio ~/.gazebo/models.

