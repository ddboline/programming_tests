#include <iostream>
 
class Muslim {  // Abstract Target
//     virtual ~Muslim() = 0;
public:
    virtual void performsMuslimRitual() = 0;
};
 
class MuslimFemale : public Muslim {  // Concrete Target
    virtual void performsMuslimRitual() override {std::cout << "Muslim girl performs Muslim ritual." << std::endl;}
};
 
class Hindu {  // Abstract Adaptee
//     virtual ~Hindu() = 0;
public:
    virtual void performsHinduRitual() = 0;
};
 
class HinduFemale : public Hindu {  // Concrete Adaptee
    virtual void performsHinduRitual() override {std::cout << "Hindu girl performs Hindu ritual." << std::endl;}
};
 
class MuslimRitual {
public:
    void carryOutRitual (Muslim* muslim) {
        std::cout << "On with the Muslim rituals!" << std::endl;
        muslim->performsMuslimRitual();
    }
};
 
class MuslimAdapter : public Muslim {  // Adapter
    private:
        Hindu* hindu;
    public:
        MuslimAdapter (Hindu* h) : hindu(h) {}
        virtual void performsMuslimRitual() override {hindu->performsHinduRitual();}
};
 
int main() {  // Client code
    HinduFemale hinduGirl;
    MuslimFemale muslimGirl;
    MuslimRitual muslimRitual;
    //muslimRitual.carryOutRitual(&hinduGirl);  // Will not compile of course since the parameter must be of type Muslim*.
    MuslimAdapter adaptedHindu(&hinduGirl);  // hinduGirl has adapted to become a Muslim!
 
    muslimRitual.carryOutRitual(&muslimGirl);
    muslimRitual.carryOutRitual(&adaptedHindu);  // So now hinduGirl, in the form of adaptedHindu, participates in the muslimRitual!
                // Note that hinduGirl is carrying out her own type of ritual in muslimRitual though.
 
}
