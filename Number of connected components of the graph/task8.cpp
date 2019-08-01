#include <iostream>
#include <cstdlib>
#include <time.h>

class Graph{
    private:
        int size;
        int zeroRarityCoeff;
        int *groups;
        int **matrix;
        int componentsCount;
        int singleNodeCount;
    public:
        Graph(int size, int coeff=2){
            srand (time(NULL));
            zeroRarityCoeff = coeff;
            this->size = size;
            groups = new int [size];
            matrix = new int* [size];
            for (int i = 0; i < size; i++)
                matrix[i] = new int [size];
            componentsCount = 0;
            singleNodeCount = 0;
        }
        ~Graph(){
            for (int i = 0; i < size; i++)
                delete matrix[i];
            delete matrix;
            delete groups;
        }
        void generateGraph(){
            for (int i = 0; i < size; i++){
                groups[i] = -1;
                for (int j = 0; j < i; j++){
                        if ((rand() % zeroRarityCoeff) == 0){
                            matrix[i][j] = 1;
                            matrix[j][i] = 1;
                        }
                        else{
                            matrix[i][j] = 0;
                            matrix[j][i] = 0;
                        }
                        matrix[i][i] = 1;
                }
            }
            matrix[0][0] = 1;
        }
        
        void setGraphFromData(int *data){
            for (int i = 0; i < size; i++){
                groups[i] = -1;
                for (int j = 0; j < size; j++)
                    matrix[i][j] = data[i*size + j];
            }
        }
        
        void printMatrix(){
            std::cout<<"N ";
            for (int i = 0; i < size; i++)
                std::cout<<i<<" ";
            std::cout<<std::endl;
            for (int i = 0; i < size; i++){
                std::cout<<i<<" ";
                for (int j = 0; j < size; j++)
                    std::cout<<matrix[i][j]<<" ";
                std::cout<<std::endl;
            }
        }
        
        void groupMerge(int oldGroupID, int newGroupID){
            for (int i = 0; i < size; i++){
                if (groups[i] == oldGroupID)
                    groups[i] = newGroupID;
            }
            componentsCount-=1;
        }
        
        void findAllNeighbours(){
            for (int i = 0; i < size; i++){
                for (int j = i; j < size; j++){
                if ((matrix[i][j] == 1) and (i != j))
                    if ((groups[i] != -1) and (groups[j] == -1))
                        groups[j] = groups[i];
                    else if ((groups[j] != -1) and (groups[i] == -1))
                        groups[i] = groups[j];
                    else if((groups[j] != -1) and (groups[i] != -1) and (groups[i] != groups[j])){
                        groupMerge(groups[j], groups[i]);
                    }
                    else if ((groups[j] == -1) and (groups[i] == -1)){
                        componentsCount +=1;
                        groups[i] = componentsCount;
                        groups[j] = componentsCount;
                    }
                }
            } 
        }
        
        void printGroups(){
            
            for (int i = 0; i < size; i++){
                if (groups[i] == -1)
                    singleNodeCount+=1;
            }
            std::cout<<"Number of connected nodes            = "<<componentsCount<<std::endl;
            std::cout<<"Number of single nodes               = "<<singleNodeCount<<std::endl;
            std::cout<<"Total number of connected components = "<<componentsCount+singleNodeCount<<std::endl;

        }
        
        
};

int main()
{
    int size = 10;
    int zeroRarityCoeff = 8;
    Graph graph {size, zeroRarityCoeff};
    graph.generateGraph();
    /*int testData[4][4] = {
        {1, 0, 0, 0},
        {0, 1, 0, 0},
        {0, 0, 1, 0},
        {0, 0, 0, 1}
    };*/
    //graph.setGraphFromData(&testData[0][0]);
    graph.printMatrix();
    graph.findAllNeighbours();
    graph.printGroups();
    return 0;
}
