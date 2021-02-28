### Laravel bulk sms

This package provides an easy inteface for sending SMS in your laravel application. Open a free account [Royce BulkSMS](http://bulksms.roycetechnologies.co.ke), under API menu click generate API. Copy the API key and paste it in your .env file

```sh
API_KEY=apikey
SENDER_ID=RoyceLTD
```

## Features

- Provide an easy interface for sending bulk sms
- Provides a database table for storing sent text.
- An interface for viewing sent text (once you install the package and ran migration visit _**/textmessages**_ url to view sent texts)
- Provide a callback URL you add to your bulksms account. This will ensure that you receive delivery status back to your application (_coming soon_)

## Installation

Require the `royceltd/laravel-bulksms` package in your `composer.json` and update your dependencies:

```sh
composer require royceltd/laravel-bulksms
```

### Integration

Add the service provider to your `config/app.php` file:

```php

    'providers'     => array(

        //...
         RoyceLtd\LaravelBulkSMS\LaravelBulkSMSServiceProvider::class,

    ),

```