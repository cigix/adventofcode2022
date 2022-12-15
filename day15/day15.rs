use std::env;
use std::fs;
use std::rc::Rc;

use regex::Regex;

#[derive(Debug, Eq, PartialEq)]
struct Point {
    x: i64,
    y: i64
}

fn manhattan(p1: &Point, p2: &Point) -> u64
{
    p1.x.abs_diff(p2.x) + p1.y.abs_diff(p2.y)
}

#[derive(Debug)]
struct Beacon {
    pos: Point
}

#[derive(Debug)]
struct Sensor {
    pos: Point,
    _closest: Rc<Beacon>,
    distance: u64
}

fn main() -> ()
{
    // Panics if no 1st or 2nd arg, and if 2nd arg is not an i32
    let filename = env::args().nth(1).unwrap();
    let queryrow = env::args().nth(2).unwrap().parse::<i64>().unwrap();

    let mut beacons: Vec<Rc<Beacon>> = Vec::new();
    let mut sensors: Vec<Sensor> = Vec::new();

    let re = Regex::new(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)").unwrap();
    for line in
        fs::read_to_string(filename)
        .unwrap()
        .split_terminator('\n')
    {
        let captures = re.captures(line).unwrap();
        let sx = captures.get(1).unwrap().as_str().parse::<i64>().unwrap();
        let sy = captures.get(2).unwrap().as_str().parse::<i64>().unwrap();
        let bx = captures.get(3).unwrap().as_str().parse::<i64>().unwrap();
        let by = captures.get(4).unwrap().as_str().parse::<i64>().unwrap();

        let sensorpos = Point{ x: sx, y: sy };
        let beaconpos = Point{ x: bx, y: by };
        let distance = manhattan(&sensorpos, &beaconpos);
        if let Some(rcb) = beacons.iter().find(|&rcb| rcb.pos == beaconpos) {
            sensors.push(Sensor {
                pos: sensorpos,
                _closest: rcb.clone(),
                distance
            });
        } else {
            let rcb = Rc::new(Beacon { pos: beaconpos });
            beacons.push(rcb.clone());
            sensors.push(Sensor {
                pos: sensorpos,
                _closest: rcb.clone(),
                distance
            });
        }
    }

    // part 1
    let minx = sensors.iter()
        // Filter all sensors whose diamond overlaps queryrow
        .filter(|&s| queryrow.abs_diff(s.pos.y) <= s.distance)
        // Get the lowest x in the diamond-queryrow overlap
        .map(|s|
             // manhattan(p1, p2) == |p1.x - p2.x| + |p1.y - p2.y|
             // p1 is s.pos, p2.y is queryrow, manhattan is s.distance, we are
             // solving for lowest possible value for p2.x
             // |s.pos.x - x| = s.distance - |s.pos.y - queryrow|
             // x = s.pos.x - (s.distance - |s.pos.y - queryrow|)
             s.pos.x - (s.distance - s.pos.y.abs_diff(queryrow)) as i64)
        .min()
        .unwrap();
    let maxx = sensors.iter()
        .filter(|&s| queryrow.abs_diff(s.pos.y) <= s.distance)
        .map(|s| s.pos.x + (s.distance - s.pos.y.abs_diff(queryrow)) as i64)
        .max()
        .unwrap();
    let beaconsonqueryrow = beacons.iter()
        .filter(|&rcb| rcb.pos.y == queryrow)
        .count();
    println!("{}", maxx - minx + 1 - beaconsonqueryrow as i64);

    // part 2
    // Only 1 solution for distress beacon => must be touching a diamond
    //let size = 20;
    let size = 4_000_000;
'outer: for sensor in sensors.iter() {
        // Loop on all candidate y positions
        let mindy = - (sensor.distance as i64) - 1;
        let maxdy = sensor.distance as i64 + 1;
        for dy in mindy ..= maxdy {
            let y = sensor.pos.y + dy;
            if y < 0 || size < y {
                continue; // this y value is outside the square
            }
            let absdx = sensor.distance as i64 - dy.abs() + 1;
            // Loop on both possible directions
            for direction in (-1 ..= 1).step_by(2) {
                let dx = absdx * direction;
                let x = sensor.pos.x + dx;
                if x < 0 || size < x {
                    continue; // this x value is outside the square
                }
                
                let pos = Point{ x, y };
                // if all sensors sense below their distance to pos
                if sensors.iter()
                    .all(|s| s.distance < manhattan(&pos, &s.pos))
                {
                    // then no sensor would sense a beacon here
                    println!("{:2}, {:2}: {}", x, y, x * 4000000 + y);
                    break 'outer;
                }
            }
        }
    }

    // Visualiser
    //let minx = sensors.iter().map(|s| s.pos.x - s.distance as i32).min().unwrap();
    //let maxx = sensors.iter().map(|s| s.pos.x + s.distance as i32).max().unwrap();
    //let miny = sensors.iter().map(|s| s.pos.y - s.distance as i32).min().unwrap();
    //let maxy = sensors.iter().map(|s| s.pos.y + s.distance as i32).max().unwrap();
    //for y in miny..=maxy {
    //    print!("{:3} ", y);
    //    for x in minx..=maxx {
    //        if x == 0 && y == 0 {
    //            print!("0");
    //            continue;
    //        }

    //        let pos = Point{ x, y };

    //        if let Some(_) = beacons.iter().find(|&rcb| rcb.pos == pos) {
    //            print!("B");
    //            continue;
    //        }
    //        if let Some(_) = sensors.iter().find(|&s| s.pos == pos) {
    //            print!("S");
    //            continue;
    //        } 
    //        if sensors.iter()
    //            .any(|s| manhattan(&pos, &s.pos) <= s.distance)
    //        {
    //            print!("#");
    //        } else {
    //            print!(".");
    //        }
    //    }
    //    println!();
    //}
}
