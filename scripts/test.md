

# Manhattan-II


[![Latest Stable Version](http://img.shields.io/github/release/jenssegers/date.svg)](https://packagist.org/packages/jenssegers/date)


echo $date->timespan(); // 3 months, 1 week, 1 day, 3 hours, 20 minutes


use Jenssegers\Date\Date;

Date::setLocale('nl');

echo Date::now()->format('l j F Y H:i:s'); // zondag 28 april 2013 21:58:16

echo Date::parse('-1 day')->diffForHumans(); // 1 dag geleden


