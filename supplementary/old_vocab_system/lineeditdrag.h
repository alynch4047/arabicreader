#include <qlineedit.h>

class lineeditdrag : public QLineEdit
   {
    Q_OBJECT
    public:
        lineeditdrag( QWidget *parent = 0);
        ~lineeditdrag() {}
    signals:
        void test();
    };
