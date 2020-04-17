#include <iostream>
#include <math.h>

using namespace std;

//общие константы:
const double G = 6.67e-11;//гравитационная постоянная
const double IG = 4600;//среднее значение удельной тяги ЖРД - отношение тяги к расходу топлива

//константы, которые я выбираю для данной конкретной задачи
const double H_START_KM = 10;//высота над поверхностью планеты в начальный момент времени
const double SPACECRAFT_MASS_KG_MIN = 5000;//масса аппарата - да, она должна быть переменной из-за расхода топлива, но нет
const double SPACECRAFT_MASS_KG_MAX = 7000;
const double PLANET_GRAV_ACCEL_MS2 = 1.6;//пусть пока как на Луне
const double LIMIT_VERTICAL_V_MSEC = 2;//лимит на вертикальную скорость при посадке, м/с
const double LIMIT_FUEL_KG = 450;//лимит на количество потраченного топлива, кг

const double ENGINE_FORCE_NEWTONS_MIN = 1 * PLANET_GRAV_ACCEL_MS2 * SPACECRAFT_MASS_KG_MIN;
const double ENGINE_FORCE_NEWTONS_MAX = 2 * PLANET_GRAV_ACCEL_MS2 * SPACECRAFT_MASS_KG_MAX;

//делаем массу переменной в зависимости от мощности двигателя
double CalcSpacecraftMassByEngine(
        double engineForceNewtons )
{
    double coeff = ( engineForceNewtons - ENGINE_FORCE_NEWTONS_MIN ) / (double)( ENGINE_FORCE_NEWTONS_MAX - ENGINE_FORCE_NEWTONS_MIN );
    double mass = SPACECRAFT_MASS_KG_MIN + coeff * ( SPACECRAFT_MASS_KG_MAX - SPACECRAFT_MASS_KG_MIN );
    return mass;
}


//расчет интервала времени свободного падения
// - от начального момента до включения тормозного посадочного двигателя
void CalcIntervalFreeFalling(
        double hStartKm,//высота над поверхностью планеты в начальный момент времени
        double hTurnOnEngineKm,//высота над поверхностью планеты в момент, когда включается движок
        double planetGravAccelMS2,//ускорение свободного падения планеты - считаем постоянным
        double* ptr_deltaT1Sec,//возвращаемое значение - продолжительность интервала в секундах
        double* ptr_V1MSec )//возвращаемое значение - вертикальная скорость снижения в момент включения движка, м/с
{
    double deltaT1Sec = sqrt( 2 * ( hStartKm - hTurnOnEngineKm ) * 1000 / planetGravAccelMS2 );

    *ptr_deltaT1Sec = deltaT1Sec;
    *ptr_V1MSec = deltaT1Sec * planetGravAccelMS2;
}

//расчет интервала работы двигателя
// - от включения тормозного двигателя до поверхности, если долетим - возвращаем true
// можем же и вверх полететь - тогда возвращаем false
bool CalcIntervalEngineWorking(
        double V1MSec,//вертикальная скорость снижения в момент включения движка, м/с
        double hTurnOnEngineKm,//высота над поверхностью планеты в момент, когда включается движок
        double engineAccelMS2,//ускорение от тяги двигателя
        double planetGravAccelMS2,//ускорение свободного падения планеты - считаем постоянным
        double *ptr_deltaT2Sec,//возвращаемое значение - продолжительность интервала работы двигателя в секундах
        double *ptr_V2MSec )//возвращаемое значение - вертикальная скорость снижения в момент касания поверхности, м/с
{
    //особый случай - если ускорение от двигателя компенсирует ускорение свободного падения,
    //то получается падение с постоянной скоростью
    if ( planetGravAccelMS2 == engineAccelMS2 )
    {
        double deltaT2Sec = hTurnOnEngineKm / V1MSec;
        double V2MSec = V1MSec;

        //cout << "Equal accelerations, one root\n";
        *ptr_deltaT2Sec = deltaT2Sec;
        *ptr_V2MSec = V2MSec;
    }
    else
    {
        //нужно решить квадратное уравнение - считаем дискриминант
        double D = V1MSec * V1MSec + 2 * ( planetGravAccelMS2 - engineAccelMS2 ) * hTurnOnEngineKm * 1000;
        if( D < 0 )
            return false;//не долетели - тяга движка слишком велика, затормозились и полетели обратно вверх

        //иначе считаем дальше - сколько времени ушло и какая скорость получилась у Земли
        double deltaT2Sec_1 = ( - V1MSec + sqrt( D ) ) / (double)( planetGravAccelMS2 - engineAccelMS2 );
        double deltaT2Sec_2 = ( - V1MSec - sqrt( D ) ) / (double)( planetGravAccelMS2 - engineAccelMS2 );

        //cout << "Roots: " << deltaT2Sec_1 << " " << deltaT2Sec_2 << "\n";

        double deltaT2Sec = deltaT2Sec_1;
        double V2MSec = V1MSec + deltaT2Sec * ( planetGravAccelMS2 - engineAccelMS2 );
        //вертикальная скорость снижения в момент касания поверхности планеты, м/с

        *ptr_deltaT2Sec = deltaT2Sec;
        *ptr_V2MSec = V2MSec;
    }

    return true;
}

//расчет затрат топлива, кг
double CalcFuelCostKg(
        double deltaTEngineSec,//продолжительность работы двигателя, сек
        double engineForceNewtons )//величина тяги двигателя, Н
{
    double fuelCostPerSecond = engineForceNewtons / IG;
    return ( fuelCostPerSecond * deltaTEngineSec );
}

//основная функция расчета - на вход получает данные от пользователя
void CommonCalculations(
        double hTurnOnEngineKm,//высота над поверхностью планеты в момент, когда включается движок
        double engineForceNewtons )//величина тяги двигателя, Н
{
    //сразу договоримся, что 0 <= hTurnOnEngineKm <= H_START_KM - ограничение "ползунка"
    // и надо выбрать ограничения для engineForceNewtons

    //обсчет участка свободного падения до включения двигателя
    double deltaT1Sec;
    double V1MSec;
    CalcIntervalFreeFalling(
            H_START_KM,//высота над поверхностью планеты в начальный момент времени
            hTurnOnEngineKm,//высота над поверхностью планеты в момент, когда включается движок
            PLANET_GRAV_ACCEL_MS2,//ускорение свободного падения планеты - считаем постоянным
            &deltaT1Sec,//возвращаемое значение - продолжительность интервала в секундах
            &V1MSec );//возвращаемое значение - вертикальная скорость снижения в момент включения движка, м/с
//    cout << "deltaT1Sec = " << deltaT1Sec
//            << " sec, V1MSec = " << V1MSec
//            << " m/s\n";

    //обсчет участка снижения с работающим двигателем
    double spacecraftMass = CalcSpacecraftMassByEngine( engineForceNewtons );
    double deltaT2Sec;
    double V2MSec;
    bool resultSecondStep = CalcIntervalEngineWorking(
            V1MSec,//вертикальная скорость снижения в момент включения движка, м/с
            hTurnOnEngineKm,//высота над поверхностью планеты в момент, когда включается движок
            engineForceNewtons / spacecraftMass,//ускорение от тяги двигателя
            PLANET_GRAV_ACCEL_MS2,//ускорение свободного падения планеты - считаем постоянным
            &deltaT2Sec,//возвращаемое значение - продолжительность интервала работы двигателя в секундах
            &V2MSec );//возвращаемое значение - вертикальная скорость снижения в момент касания поверхности, м/с

//    cout << "H = " << hTurnOnEngineKm << " km, F = "
//         << engineForceNewtons << " N, mass = "
//         << spacecraftMass << " kg: ";
    if( resultSecondStep == false )
    {
        //cout << "Surface not achieved - flying up\n";//сообщение, что взлетаем, не достигнув поверхности планеты
    }
    else
    {
        double fuelCostKg = CalcFuelCostKg(
                deltaT2Sec,//продолжительность работы двигателя, сек
                engineForceNewtons );//величина тяги двигателя, Н

        if( ( V2MSec < LIMIT_VERTICAL_V_MSEC )&&( fuelCostKg < LIMIT_FUEL_KG ) )
        {
            cout << "H = " << hTurnOnEngineKm << " km, F = "
                 << engineForceNewtons << " N, mass = "
                 << spacecraftMass << " kg: ";
            cout << "deltaT2Sec = " << deltaT2Sec
                    << " sec, V2MSec = " << V2MSec
                    << " m/s, fuel = " << fuelCostKg << " kg\n";
        }
    }
}


int main()
{
    int iQuantity = 1000;
    double hStep = ( H_START_KM - 0 )/ (double)iQuantity;

    int jQuantity = 1000;
    double engineForceStep = ( ENGINE_FORCE_NEWTONS_MAX - ENGINE_FORCE_NEWTONS_MIN ) / (double)jQuantity;

    //внешний цикл - перебор значений высоты
    for( int i = 0; i < iQuantity; i++ )
    {
        double hTurnOnEngineKm = 0 + hStep * i;

        //внутренний цикл - перебор значений тяги двигателя
        for( int j = 0; j < jQuantity; j++ )
        {
            double engineForceNewtons = ENGINE_FORCE_NEWTONS_MIN + engineForceStep * j;
            CommonCalculations(
                    hTurnOnEngineKm,//высота над поверхностью планеты в момент, когда включается движок
                    engineForceNewtons );//величина тяги двигателя, Н
        }
    }


    return 0;
}
