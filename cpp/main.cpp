#include <QApplication>
#include <QStringList>
#include <QCheckBox>
#include <QComboBox>
#include <QVBoxLayout>
#include <QWidget>

#include "io.h"

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    QWidget window;
    QVBoxLayout *layout = new QVBoxLayout(&window);

    layout->addWidget(new QCheckBox("click me"));

    QComboBox *cobobox = new QComboBox();

    // Convert std::vector<std::string> to QStringList
    std::vector<std::string> models_std = list_models();
    QStringList models_qt;
    for (const auto &m : models_std) {
        models_qt << QString::fromStdString(m);
    }

    cobobox->addItems(models_qt);
    layout->addWidget(cobobox);

    window.resize(600, 400);
    window.show();

    return app.exec();
}

