#include <iostream>
#include <cstdlib>
#include <time.h>
#include <stack> 

using namespace std;

class Map{
    private:
        int size;
        char **field;
        short **turnsToReach;
        int inX, inY, tgX, tgY;
        bool targetPresent, initialPresent;
    public:
        Map(int size){
            srand (time(NULL));
            this->size = size;
            field = new char* [size];
            for (int i = 0; i < size; i++)
                field[i] = new char [size];
            
            turnsToReach = new short* [size];
            for (short i = 0; i < size; i++)
                turnsToReach[i] = new short [size];
            clearMap();
        }
        
        ~Map(){
            for (int i = 0; i < size; i++){
                delete field[i];                
                delete turnsToReach[i];}
            delete field;
            delete turnsToReach;
        }
        
        void clearMap(){
            for (int i = 0; i < size; i++){
                for (int j = 0; j < size; j++){
                    field[i][j] = 0;  
                    turnsToReach[i][j] = -1;}
            }     
            targetPresent = false;
            initialPresent = false;
            inX = -1;
            inY = -1;
            tgX = -1;
            tgY = -1;
        }
        
        void printMap(){
            for (int i = 0; i < size; i++){
                for (int j = 0; j < size; j++)
                    std::cout<<field[i][j]<<" ";
                std::cout<<std::endl;
            }
        }
        
        void printReachability(){
            for (int i = 0; i < size; i++){
                for (int j = 0; j < size; j++)
                    std::cout<<turnsToReach[i][j]<<" ";
                std::cout<<std::endl;
            }
        }
        
        void setMapFromData(char *data){
            for (int i = 0; i < size; i++)
                for (int j = 0; j < size; j++)
                    field[i][j] = data[i*size + j];
        }
        
        void setMapRandom(){
            for (int i = 0; i < size; i++)
                for (int j = 0; j < size; j++){
                    if (field[i][j] != '@' or field[i][j] != '*')
                        if (rand() % 2 == 0)
                            field[i][j] = '0';
                        else
                            field[i][j] = '1';
                }
        }
        
        void setSingleFieldManual(int x, int y, char symbol){
            if (x < size and y < size)
                field[x][y] = symbol;
            if (x == inX and y == inY)
                initialPresent = false;
            if (x == tgX and y == tgY)
                targetPresent = false;    
        }
        
        void setInitialPosition(int inX, int inY){
            if (inX < size and inY < size and field[inX][inY] == '0'){
                field[inX][inY] = '@';
                turnsToReach[inX][inY] = 0;
                this->inX = inX;
                this->inY = inY;
                initialPresent = true;
            }
            else
                std::cout<<"ERROR: field is not empty, or position is out of range. Consider manual cleaning, if that is the case\n";
        }
        
        void setTargetPosition(int tgX, int tgY){
            if (tgX < size and tgY < size and field[tgX][tgY] == '0'){
                field[tgX][tgY] = '*';
                this->tgX = tgX;
                this->tgY = tgY;
                targetPresent = true;
            }
            else
                std::cout<<"ERROR: field is not empty, or position is out of range. Consider manual cleaning, if that is the case\n";
        }
        
        pair<pair<int,int>,pair<int,int>> returnMapState(){
            std::cout<<"Target present = "<<targetPresent<<std::endl;
            if (targetPresent)
                std::cout<<"on position ("<<tgX<<" "<<tgY<<")\n";
            else
                std::cout<<"Actualy, not present"<<std::endl;
            std::cout<<"Initial present = "<<initialPresent<<std::endl;
            if (initialPresent)
                std::cout<<"on position ("<<inX<<" "<<inY<<")\n";
            else
                std::cout<<"Actualy, not present"<<std::endl;
            return make_pair(make_pair(inX,inY),make_pair(tgX,tgY));
        }
        
        bool mapReady(){
            if (initialPresent and targetPresent)
                return true;
            else
                return false;
        }
        
        char **returnField(){
            return field;
        }
        
        short **returnTurnsToReach(){
            return turnsToReach;
        }
        
        pair<int,int> returnInitial(){
            return pair<int,int>(inX,inY);
        } 
        
        short returnStepsToGoal(){
            return turnsToReach[tgX][tgY];
        } 
}; 

class Wayfinder{
    private:
        int size;
        int inX, inY, tgX, tgY;
        int cX, cY;
        short moveCount;
        stack <pair<int,int> > positionToCheck;
    public:
        Wayfinder(int size, int inX, int inY, int tgX, int tgY){
            this->size = size;
            this->inX = inX;
            this->inY = inY;
            this->tgX = tgX;
            this->tgY = tgY;
            cX = inX;
            cY = inY;
            moveCount = 0;
        }
        
        short checkLine(int X, int Y, char direction, char **field, short **turnsToReach){
            //std::cout<<moveCount<<" "<<direction<<" "<<X<<" "<<Y<<" "<<field[X][Y]<<std::endl;
            int dirX = 0; int dirY = 0;
            int curX = X; int curY = Y;
            short currentTurnCount = 1 + turnsToReach[X][Y];
            while((curX!= -1) and (curX!= size+1) and (curY!= -1) and (curY!= size+1)){
                curX += dirX;
                curY += dirY;            
            if (direction == 'U'){
                if (curX == 0){
                    //std::cout<<"No fields in that direction\n";
                    return -1;
                } else   
                dirX = -1;
            } else if (direction == 'D'){
                if (curX == size){
                    //std::cout<<"No fields in that direction\n";
                    return -1;
                } else  
                dirX = 1;
            } else if (direction == 'L'){
                if (curY == 0){
                    //std::cout<<"No fields in that direction\n";
                    return -1;
                } else  
                dirY = -1;
            } else if (direction == 'R'){
                if (curY == size){
                    //std::cout<<"No fields in that direction\n";
                    return -1;
                } else  
                dirY = 1;
            }
                if ((curX == tgX) and (curY == tgY)){
                    //std::cout<<"Target Reached\n";
                    if((turnsToReach[curX][curY] > currentTurnCount) or (turnsToReach[curX][curY]==-1)){
                        turnsToReach[curX][curY] = currentTurnCount;
                    }
                } else if (field[curX][curY] == '1'){
                    //std::cout<<"Wall Reached\n";
                    return -1;
                } else {
                    if (turnsToReach[curX][curY] == -1){
                        turnsToReach[curX][curY] = currentTurnCount;
                        positionToCheck.push(make_pair(curX, curY));
                    } else if(turnsToReach[curX][curY] > currentTurnCount){
                        turnsToReach[curX][curY] = currentTurnCount;
                        positionToCheck.push(make_pair(curX, curY));
                    }
                }
            }
        }
        
        short findWay(char **field, short **turnsToReach){
            positionToCheck.push(make_pair(inX, inY));
            while(!positionToCheck.empty()){
                pair<int,int> coordsToCheck;
                coordsToCheck = positionToCheck.top();
                positionToCheck.pop();
                checkLine(coordsToCheck.first, coordsToCheck.second, 'U', field, turnsToReach);
                checkLine(coordsToCheck.first, coordsToCheck.second, 'D', field, turnsToReach);
                checkLine(coordsToCheck.first, coordsToCheck.second, 'L', field, turnsToReach);
                checkLine(coordsToCheck.first, coordsToCheck.second, 'R', field, turnsToReach);
            }
        }
        
};

int main()
{
    int size = 5;
    Map map {size};
    //map.setMapRandom();
    char data[size][size] = {
        {'0', '0', '0', '0', '0'},
        {'1', '1', '1', '1', '0'},
        {'1', '0', '1', '0', '0'},
        {'1', '0', '1', '1', '0'},
        {'1', '0', '0', '0', '0'}
    };
    map.setMapFromData(&data[0][0]);
    map.setSingleFieldManual(0,0,'0');
    map.setInitialPosition(0,0);
    map.setSingleFieldManual(2,1,'0');
    map.setTargetPosition(2,1);
    //map.printMap();
    if (map.mapReady()){
        auto p = map.returnMapState();
        Wayfinder wf {size, p.first.first, p.first.second, p.second.first, p.second.second};
        wf.findWay(map.returnField(), map.returnTurnsToReach());
        if (map.returnStepsToGoal() != -1)
            std::cout<<"Number of moves: "<<map.returnStepsToGoal()<<std::endl;
        else
            std::cout<<"No way!"<<std::endl;
    } else {
        std::cout<<"Map not ready!\n";
    }
    std::cout<<"Map "<<std::endl;
    map.printMap();
    std::cout<<"Reachability map "<<std::endl;
    map.printReachability();
    return 0;
}
