# tasks from postgresql introbook, "demo" database 

# aircraft`s model and code with seats on aircraft available

with gb as 
(
	select ac.aircraft_code, count(*) 
		from aircrafts ac 
		join seats s 
		on ac.aircraft_code = s.aircraft_code 
		group by ac.aircraft_code
)
select ac.model, gb.* from aircrafts ac 
	join gb 
	on gb.aircraft_code = ac.aircraft_code;


# how many free places were yesterday at PG0404 flight

with occupied as
(
	select count(*)
	from boarding_passes bp
	join flights fl
	on fl.flight_id = bp.flight_id
	where fl.flight_no = 'PG0404' 
	AND fl.scheduled_departure::date = bookings.now()::date - INTERVAL '1 day' 
),
	amount as
(
	select count(*)
	from aircrafts ac
	join seats s
	on ac.aircraft_code = s.aircraft_code
	join flights fl
	on fl.aircraft_code = ac.aircraft_code
	where fl.scheduled_departure::date = bookings.now()::date - INTERVAL '1 day'
	AND fl.flight_no = 'PG0404'
	group by ac.aircraft_code
)

select (select * from amount) - (select * from occupied) as free;

# most long delays

select fl.actual_departure - fl.scheduled_departure as delay 
	from flights fl 
	where fl.actual_departure is not null and fl.status in ('Departed', 'Arrived')
order by dif desc limit 10;

# min, max fligh duration with info about delays group by flights from MSC to SPB

with flights_with_condition as
(
	select 
		
		fl.flight_no as flno, ap_d.city as departure, ap_a.city as arrival, fl.scheduled_departure as sch_d,

		case when fl.actual_departure is not null then fl.actual_departure
		else fl.scheduled_departure
		end as dtime, 

		case when fl.actual_arrival is not null then fl.actual_arrival
		else fl.scheduled_arrival
		end as atime

	from flights fl
	join airports ap_d on fl.departure_airport = ap_d.airport_code
	join airports ap_a on fl.arrival_airport = ap_a.airport_code
	where ap_d.city = 'Москва' AND ap_a.city = 'Санкт-Петербург'
)

select flno, min(fl.atime - fl.dtime) as "min duration", 
			max(fl.atime - fl.dtime) as "max duration", 
			sum(case when (dtime - fl.sch_d) > INTERVAL '1 hour' then 1 else 0 end) as delay,
			sum(case when (dtime - fl.sch_d) < INTERVAL '1 hour' then 1 else 0 end) as "in_time"
	from flights_with_condition fl group by fl.flno;


