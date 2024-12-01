using System.ComponentModel;
using System.Reflection;
using Aoc.Shared.Abstract;
using Autofac;

namespace Aoc._2024;

class Program
{
    static void Main(string[] args)
    {
        var container = BuildContainer();

        container.Resolve<IAocSolutionRunner>().RunPart1();
        container.Resolve<IAocSolutionRunner>().RunPart2();
    }

    private static Autofac.IContainer BuildContainer()
    {
        var builder = new ContainerBuilder();

        builder.RegisterType<AocSolutionRunner>().As<IAocSolutionRunner>();


        builder.RegisterAssemblyTypes(Assembly.GetExecutingAssembly())
            .Where(type => type.IsAssignableTo(typeof(IAocSolution)))
            .AsImplementedInterfaces();

        return builder.Build();
    }
}