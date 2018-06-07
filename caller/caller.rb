require 'json'

def call(interpreter, filepath, *args)
  ret = ''
  cmd = ([interpreter, filepath] + args).join(' ')
  begin
    # ret = IO.popen(cmd).gets
    ret = `#{cmd}`
  rescue Exception => e
    puts "Error while executing: #{cmd}"
    puts e.message
    puts e.backtrace.inspect
    ret = ''
  ensure
    # TODO, I dont know what to do.
  end
  # print(cmd)
  ret.gsub!('\'', '"')
  ret = JSON.parse(ret)
  return ret
end

def call_py(filepath, *args)
  interpreter = 'python'
  return call(interpreter, filepath, args)
end