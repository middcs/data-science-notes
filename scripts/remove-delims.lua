-- after https://github.com/insightsengineering/pattern-strip/blob/main/_extensions/pattern-strip/pattern-strip.lua

return {
    {
        CodeBlock = function(el)
            
            -- quarto.log.output(el)
            
            local lines = pandoc.List()
            local code = el.text .. "\n"

            for line in code:gmatch("([^\n]*)\n") do
                line, _ = line:gsub("#%-%-%-","")
                lines:insert(line)
            end

            lines:insert(line)

            el.text = table.concat(lines, "\n")

            return el
            
        end
    }
}

