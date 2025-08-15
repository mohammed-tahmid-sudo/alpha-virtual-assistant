cmake_minimum_required(VERSION 3.10)
project(VirtualAssistant)

set(CMAKE_CXX_STANDARD 17)

# Find Qt libraries
find_package(Qt6 COMPONENTS Core Widgets REQUIRED)
find_package(Python3 COMPONENTS Development REQUIRED)

# Add source files
set(SOURCES
    main.cpp
    audio_capture.cpp
    wake_word.cpp
    command_parser.cpp
    desktop_control.cpp
    iot_control.cpp
    model_bridge.cpp
)

# Create executable
add_executable(virtual_assistant ${SOURCES})

# Include directories
target_include_directories(virtual_assistant PRIVATE ${Python3_INCLUDE_DIRS})

# Link libraries
target_link_libraries(virtual_assistant
    PRIVATE Qt6::Core Qt6::Widgets ${Python3_LIBRARIES}
)

# Enable Qt's automatic MOC, UIC, and RCC
set_target_properties(virtual_assistant PROPERTIES
    AUTOMOC ON
    AUTOUIC ON
    AUTORCC ON
)
add_custom_target(run
    COMMAND virtual_assistant
    DEPENDS virtual_assistant
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
)

