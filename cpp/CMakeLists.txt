cmake_minimum_required(VERSION 3.16)
project(VirtualAssistant LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 REQUIRED COMPONENTS Core Widgets)
find_package(Python3 REQUIRED COMPONENTS Development)

# Collect all .cpp files from each component folder
file(GLOB SOURCES
    main.cpp
    stt_tts/*.cpp
    wake_word/*.cpp
    command_parser/*.cpp
    desktop_control/*.cpp
    iot_control/*.cpp
    model_bridge/*.cpp
    io/*.cpp
)

add_executable(virtual_assistant ${SOURCES})

# Include directories
target_include_directories(virtual_assistant PRIVATE
    ${Python3_INCLUDE_DIRS}
    io
    command_parser
    desktop_control
    iot_control
    stt_tts
    wake_word
    model_bridge
)

# Link Qt and Python
target_link_libraries(virtual_assistant
    PRIVATE Qt6::Core Qt6::Widgets ${Python3_LIBRARIES}
)

# Qt auto features
set_target_properties(virtual_assistant PROPERTIES
    AUTOMOC ON
    AUTOUIC ON
    AUTORCC ON
)

# Run target
add_custom_target(run
    COMMAND virtual_assistant
    DEPENDS virtual_assistant
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
)

