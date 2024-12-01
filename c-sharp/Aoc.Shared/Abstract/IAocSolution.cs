namespace Aoc.Shared.Abstract;

public interface IAocSolution
{

    public int Day { get; }
    public string Part1();

    public string Part2();
}