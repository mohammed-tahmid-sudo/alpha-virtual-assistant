#include <QApplication>
#include <QStringList>
#include <QCheckBox>
#include <QComboBox>
#include <QHBoxLayout>
#include <QListWidget>
#include <QPushButton>
#include <QStackedWidget>
#include <QVBoxLayout>
#include <QWidget>

int main(int argc, char *argv[]) {
  QApplication app(argc, argv);

  QWidget window;
  QVBoxLayout *layout = new QVBoxLayout(&window);
  layout->addWidget(new QCheckBox("click me"));

  QComboBox *cobobox = new QComboBox();
  QStringList models = {"llama", "ollama"};
  cobobox->addItems(models);

  layout->addWidget(cobobox);

  window.resize(600, 400);
  window.show();

  return app.exec();
}
