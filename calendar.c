#include <stdio.h>

int days[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

int _days_until_month[2][12]={{0}, {0}};

void initialize(){
    for (int i=1; i<12; i++){
        _days_until_month[0][i] = _days_until_month[0][i-1] + days[i-1];
        _days_until_month[1][i] = _days_until_month[1][i-1] + days[i-1] + (i==2);
    }
}

int is_leap_year(int x){
    return (x%4==0)^(x%100==0)^(x%400==0);
}

int days_of_month(int m, int year){
    return days[m-1] + (m==2 && is_leap_year(year));
}

int days_until_month(int m, int year){
    // Since year-01-01
    return _days_until_month[is_leap_year(year)][m-1];
}

int leap_years_until(int x){
    // Number of leap years since 0001
    // leap_years_until(i) - leap_years_until(j) is # of leap years in [j, i)
    return (x-1)/4-(x-1)/100+(x-1)/400-(x<1);
}

int days_until_year(int x){
    // Since 0001-01-01
    return 365 * (x-1) + leap_years_until(x);
}

int days_until(int year, int month, int day){
    return days_until_year(year) + days_until_month(month, year) + day - 1;
}

int day_of_date(int year, int month, int day){
    return (days_until(year, month, day)+1)%7;
}

char *tian[] = {"日", "一", "二", "三", "四", "五", "六"};

void main(){
    initialize();
    for (int i=1978; i<2020; i++){
        printf("%d年1月1日是周%s\n", i, tian[day_of_date(i, 1, 1)]);
    }
}
