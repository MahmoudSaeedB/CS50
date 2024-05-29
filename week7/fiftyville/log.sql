s-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Givens: 
    -- Theft took place on July 28, 2021.
    -- It took place on Humphrey Street.

-- Find crime scene description.
SELECT description FROM crime_scene_reports 
 WHERE year = 2021 
   AND month = 7 
   AND day = 28
   AND street = 'Humphrey Street';

-- According the crime scene description:
    -- Theft took place at 10:15 a.m on the Humphrey Street bakery.
    -- Each of the three wintnesses' interview transscripts mentions the bakery. 

-- Get information from witnesses on the crime day.
SELECT name, transcript 
  FROM interviews 
 WHERE year = 2021 
   AND month = 7 
   AND day = 28 
   AND transcript LIKE '%bakery%';

-- According to the witnesses: 
    -- Within 10 minutes of the theft, the theif got in the bakery lot and drove away.
    -- The thief withdrew some money on the crime day from ATM on Leggett Street.
    -- The thief called someone who talked to them for less than a minute as he was leaving the backery.
    -- The thief said they were planning to take the earliest flight out of Fiftyville on the day after the crime day.

-- Find the theif.
-- Select the suspects.
SELECT name
  From people
  -- Eliminate people who didn't call someone for less than a minute in the crime day.
 WHERE phone_number IN
    (SELECT caller 
       FROM phone_calls
      WHERE year = 2021
        AND month = 7 
        AND day = 28 
        AND duration < 60
    )
    -- Eliminate people who didn't exit the backery within 10 minutes of the crime
   AND license_plate IN
        (SELECT license_plate 
           FROM people 
          WHERE license_plate IN 
            (SELECT license_plate 
               FROM bakery_security_logs
              WHERE year = 2021 
                AND month = 7 
                AND day = 28
                AND hour = 10 
                AND minute > 15 
                AND minute <= 25
                AND activity = 'exit'
            )
        )
        -- Eliminate people who did not withdrew money on the crime day from ATM on Leggett Street.
   AND id IN 
    (SELECT person_id 
    FROM bank_accounts 
   WHERE account_number IN 
    (SELECT account_number 
       FROM atm_transactions 
      WHERE year = 2021 
        AND month = 7 
        AND day = 28 
        AND atm_location = 'Leggett Street' 
        AND transaction_type = 'withdraw'
    )
    )
    -- Eliminate people who did not take the earliest flight out of Fiftyville on the day after the crime day.
   AND passport_number IN 
        (SELECT passport_number 
           FROM passengers 
          WHERE flight_id IN 
            (SELECT id 
               FROM flights 
              WHERE year = 2021 
                AND month = 7 
                AND day = 29 
              ORDER BY hour 
              LIMIT 1
            )
        );

-- Find the accomplice. 
-- Select the suspects.
SELECT name 
  FROM people 
  -- Elinate people who didn't recieve a call from the theif on the crime day that took less than a minute
 WHERE phone_number = 
  (SELECT receiver 
    FROM phone_calls 
   WHERE year = 2021 
     AND month = 7 
     AND day = 28 
     AND duration < 60 
     And caller = 
      (SELECT phone_number From people WHERE phone_number IN
        (SELECT caller FROM phone_calls
          WHERE year = 2021 
            AND month = 7 
            AND day = 28 
            AND duration < 60
        ) 
         And name = 'Bruce'
      )
  );

-- Find the destination.
-- Select possible destinations
SELECT city 
  FROM airports 
  -- Eliminate the destinationes of the flights other than the earliest flight going out of Fiftyville on the day after the crime day.
 WHERE id = 
  (SELECT destination_airport_id 
     FROM flights 
    WHERE year = 2021 
      AND month = 7 
      AND day = 29 
    ORDER BY hour 
    LIMIT 1
  );