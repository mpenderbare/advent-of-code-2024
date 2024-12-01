using System.Diagnostics;

namespace Aoc.Shared.Abstract;

public class AocSolutionRunner : IAocSolutionRunner
{
    private readonly IEnumerable<IAocSolution> aocSolutions;
    private readonly int latestDay;

    public AocSolutionRunner(IEnumerable<IAocSolution> aocSolutions)
    {
        this.aocSolutions = aocSolutions;
        this.latestDay = aocSolutions.Max(x => x.Day);
    }
    
    public void RunPart1(int day = -1) => RunPart(day < 0 ? latestDay : day, true);

    public void RunPart2(int day = -1)=> RunPart(day < 0 ? latestDay : day, false);

    private IAocSolution ResolveSolution(int day)
    {
        if(!aocSolutions.Any(x => x.Day == day))
            throw new NotImplementedException($"Day {day} has not been implemented.");

        return aocSolutions.First(x => x.Day == day);
    }

    private void RunPart(int day, bool part1)
    {
        var sw = new Stopwatch();

        var solution = ResolveSolution(day);

        Func<string> func = part1 ? solution.Part1 : solution.Part2;

        sw.Start();
        var result = func();
        
        Console.WriteLine($"Day {day} - Part {(part1 ? 1 : 2)}");
        Console.WriteLine($"=========================");
        Console.WriteLine($"Result = {result}");
        Console.WriteLine($"Completed in {sw.ElapsedMilliseconds} ms.");
        Console.WriteLine($"=========================");
    }
}