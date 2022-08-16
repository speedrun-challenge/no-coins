import {MinuteSecondsPipe} from './minute-seconds.pipe';

describe('MinuteSecondsPipe', () => {
  it('should convert seconds', () => {
    const pipe = new MinuteSecondsPipe();
    expect(pipe.transform(76.123)).toBe('1:16:123');
  });
});
