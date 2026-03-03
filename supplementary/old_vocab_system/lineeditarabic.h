#include <qlineedit.h>

class lineeditarabic : public QLineEdit
   {
    Q_OBJECT
    public:
        lineeditarabic( QWidget *parent = 0);
        ~lineeditarabic() {}
    signals:
        void test();
    };
