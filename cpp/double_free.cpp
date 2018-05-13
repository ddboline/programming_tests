#include <iostream>
using std::cout;
using std::cin;
using std::endl;

int MAX_SCORE = 100;

int loadTestScores(int **ptr, int numberTests=0) {
    if (numberTests == 0) {
        cout << "Enter the amount of test scores you would like to average: ";

        cin >> numberTests;
    }

    *ptr = new int[numberTests];

    for (int i = 0; i < numberTests; i++) {

        *(*ptr + i) = 1 + rand() % MAX_SCORE;

        cout << *(*ptr + i) << " ";
    }
    cout << endl;

    return numberTests;
}

double average_test_scores(int **ptr, int ptr_len) {
    double avg_score = 0;
    for (int i=0; i < ptr_len; i++) {
        avg_score += *(*ptr + i);
    }
    return avg_score / ptr_len;
}

int main(int argc, char ** argv){

    int numberTests = 0;

    if (argc > 1) {
        try {
            numberTests = atoi(argv[1]);
        } catch(std::invalid_argument) {}
    }

    int * scores = nullptr;

    int numTests = loadTestScores(&scores, numberTests);

    cout << numTests << " " << average_test_scores(&scores, numTests) << endl;
}//end main
