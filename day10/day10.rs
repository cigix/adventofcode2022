use std::env;
use std::fs;

/// Panics: if `cycles` is empty
fn noop(cycles : &mut Vec<i32>) -> ()
{
    cycles.push(*cycles.last().unwrap());
}

/// Panics: if `cycles` is empty
fn addx(cycles : &mut Vec<i32>, x : i32) -> ()
{
    let last = *cycles.last().unwrap();
    cycles.push(last);
    cycles.push(last + x);
}

fn main()
{
    // Panics if no 1st arg
    let filename = env::args().nth(1).unwrap();

    let mut cycles : Vec<i32> = vec![1];

    for instruction in
        fs::read_to_string(filename)
        .unwrap()
        .split_terminator('\n')
    {
        if instruction == "noop" {
            noop(&mut cycles);
        } else if instruction.starts_with("addx ") {
            let x = instruction[5..].parse::<i32>().unwrap();
            addx(&mut cycles, x);
        } else {
            panic!()
        }
    }

    println!("{}",
             cycles.iter()
             .enumerate()
             .skip(19) // 0 based
             .step_by(40)
             .map(|(i, x)| (i as i32 + 1) * x)
             .sum::<i32>()); // part 1

    for (cycle, x) in cycles.iter().enumerate()
    {
        let cycle = cycle as i32;
        if *x - 1 <= cycle % 40 && cycle % 40 <= *x + 1 {
            print!("#");
        } else {
            print!(".");
        }
        if cycle % 40 == 39 {
            println!();
        }
    }
}
